import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

def enrich_transaction(description: str, amount: float) -> dict:
    prompt = f"""
You are a financial assistant.

Classify the following transaction and explain if it's suspicious.
Return only valid JSON in the following format:

```json
{{
  "category": "one of: food, transport, shopping, rent, fuel, travel, others",
  "suspicious_reason": "null if not suspicious, otherwise a short explanation"
}}
Transaction: "{description}" worth ₹{amount}"

If unsure, set category to "others" and suspicious_reason to null.
"""
    # Call Gemini
    response = model.generate_content(prompt)
    return parse_llm_json(response.text)

def parse_llm_json(text: str) -> dict:
    try:
        
        if text.startswith("json"):
            text = text[len("json"):].strip()
        elif text.startswith("```json"):
            text = text[len("```json"):].strip()
        text = text.strip("`\n ")

        return json.loads(text)
    except Exception as e:
        print("⚠️ Error parsing LLM response:", text)
        return {
            "category": "others",
            "suspicious_reason": "error parsing response"
        }

if __name__ == "__main__":
    txn = enrich_transaction("Uber to Airport", 325)
    print(txn)