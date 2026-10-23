import os
from dotenv import load_dotenv
from groq import Groq

# Force reloading the .env file to override cached terminal variables
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
# Default explicitly to 'openai/gpt-oss-120b'
model_name = os.getenv("LLM_MODEL", "openai/gpt-oss-120b").strip()

if not api_key:
    print("❌ GROQ_API_KEY is missing from your .env file!")
else:
    client = Groq(api_key=api_key)
    
    print(f"Testing primary LLM model: '{model_name}'...")

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Confirm if you are connected and ready to act as the primary LLM for an Enterprise Hybrid RAG system.",
                }
            ],
            model=model_name,
        )

        print("\n✅ Primary LLM Test Successful!")
        print(f"Active Model: {model_name}")
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")