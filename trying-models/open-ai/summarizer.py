import os
from openai import OpenAI

client = OpenAI(api_key="")

def summarize_text(text, summary_type="concise"):
    """
    Summarizes text using the OpenAI API.
    
    Args:
        text (str): The text to summarize.
        summary_type (str): formatting instruction (e.g., "3 bullet points", "one sentence").
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that summarizes text."
                },
                {
                    "role": "user", 
                    "content": f"Please summarize the following text. Format the summary as {summary_type}:\n\n{text}"
                }
            ],
            temperature=0.7, 
        )
        
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    text = str(input("Enter the text to summarize: "))
    sample_text = text
    
    print("--- Generating Summary ---")
    summary = summarize_text(sample_text, summary_type="concice")
    print(summary)
