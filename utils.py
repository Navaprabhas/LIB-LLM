import os
import httpx

# Groq API configuration
groq_api_key = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

if not groq_api_key:
    raise EnvironmentError("GROQ_API_KEY is not set in environment variables.")

headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json"
}


def run_llm(prompt: str, model: str = "llama3-8b-8192") -> str:
    """
    Send prompt to Groq API and return text response.
    """
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for books and summaries."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        resp = httpx.post(GROQ_ENDPOINT, json=payload, headers=headers, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Error from LLM: {e}"