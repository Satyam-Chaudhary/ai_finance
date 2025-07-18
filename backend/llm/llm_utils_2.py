import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  
)

def enrich_transaction2(description: str, amount: float) -> dict:
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

    completion = client.chat.completions.create(
        model="moonshotai/kimi-k2:free",
        messages=[{"role": "user", "content": prompt}],
    )

    return parse_llm_json(completion.choices[0].message.content)

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
