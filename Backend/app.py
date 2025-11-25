from openai import OpenAI
import os
import pandas as pd
# from dotenv import load_dotenv
from flask import Flask, jsonify, request

# load_dotenv()

app = Flask(__name__)

# Connect to OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Example route to process uploaded dataset
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Load CSV
        file_path = request.json.get("file_path")
        df = pd.read_csv(file_path)

        # Summarize first few rows to feed into ChatGPT
        summary = df.describe().to_string()

        # Send to GPT model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a motorsport data analyst."},
                {"role": "user", "content": f"Analyze this race data:\n{summary}"}
            ]
        )

        analysis = response.choices[0].message.content
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
