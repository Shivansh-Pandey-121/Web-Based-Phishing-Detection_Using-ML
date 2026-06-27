import os
import sys
from dotenv import load_dotenv
from google import genai

# Load environment configuration variables
print("--- ⚙️ ENVIRONMENT CHECKING ---")
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: Your script cannot find 'GEMINI_API_KEY' inside your .env file.")
    print("Make sure your file is named precisely '.env' and placed in the same directory.")
    sys.exit(1)
else:
    print(f"✅ Key detected successfully: {api_key[:8]}...{api_key[-4:]}")

print("\n--- 🚀 API TEST STARTING (SDK v2) ---")

try:
    # Initialize the modern SDK client with the correct key structure
    client = genai.Client(api_key=api_key)
    print("Step 1: Google GenAI Client initialized successfully.")

    print("Step 2: Connecting to Gemini Servers...")
    # FIX: Pointing to the active gemini-2.5-flash standard deployment
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents="Reply with the exact words: CONNECTION SUCCESSFUL"
    )

    print("\n✅ RESULT: API CONNECTION SUCCESSFUL!")
    print(f"🤖 Gemini says: {response.text}")

except Exception as e:
    print("\n❌ RESULT: API CONNECTION FAILED AT SERVERS!")
    print("🚨 THE EXACT ERROR REPORTED IS:")
    print(f"-> {e}")
    print(f"Error Structural Type: {type(e).__name__}")

print("\n--- 🏁 API TEST FINISHED ---")