import os
from openai import OpenAI
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_data(text_summary):
    """Send a small summary of your race data to ChatGPT."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a race data analyst."},
            {"role": "user", "content": f"Analyze this race data:\n{text_summary}"}
        ]
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    test_summary = "Driver A: 1:23, 1:21, 1:22\nDriver B: 1:24, 1:25, 1:23"
    result = analyze_data(test_summary)
    print(result)
