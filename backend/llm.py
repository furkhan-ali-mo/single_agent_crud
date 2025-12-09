import os
import json
import google.generativeai as genai
from dotenv import load_dotenv, dotenv_values

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Temporary: List available models
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)


def analyze_intent(user_message: str) -> dict:
    """
    Analyzes the user message to extract intent and structured data using Gemini.
    """
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    
    system_prompt = """
    You are a structured-output agent.
    For any user message, return ONLY JSON:
    {
      "intent": "create" | "read" | "update" | "delete" | "unknown",
      "name": string | null,
      "email": string | null,
      "phone": string | null,
      "id": string | null
    }
    If user intent cannot be mapped to CRUD, return intent = "unknown".
    Do not include markdown formatting like ```json ... ```. Just the raw JSON string.
    """
    
    try:
        response = model.generate_content(f"{system_prompt}\n\nUser Message: {user_message}")
        response_text = response.text.strip()
        print(response_text)
        
        # Clean up potential markdown code blocks if the model ignores the instruction
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        return json.loads(response_text)
    except Exception as e:
        print(f"Error in analyze_intent: {e}")
        return {
            "intent": "unknown",
            "name": None,
            "email": None,
            "phone": None,
            "id": None
        }
