from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent

#setting up API
import os
from dotenv import load_dotenv
load_dotenv()
ANTHROPiC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

#config model
model = init_chat_model(
    "claude-sonnet-4-5-20250929",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)

#Prompt
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

#context schema 
@dataclass
class Context:
    """Custom runtime context schema"""
    user_id: str

#tools
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}!!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Reyrieve user infprmation based on user ID"""
    user_id = runtime.context.user_id
    return "New Delhi" if user_id == "1" else "Mumbai"

#response
@dataclass
class ResponseFormat:
    """Response schema for the agent"""
    punny_response: str
    weather_condition = str 

#memory
checkpointer = InMemorySaver()

#create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

#Run Agent
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_respnse'])

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Thankyou!!"}]},
    config=config,
    context=Context(user_id="1")
)
print(response["structured_response"])