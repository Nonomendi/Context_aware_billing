import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from db_tools import get_customer_details, update_customer_tier

# Load environment variables
load_dotenv()

# Pull the API key dynamically from your system environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

my_billing_tools = [get_customer_details, update_customer_tier]

chat = client.chats.create(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are an expert customer billing assistant with advanced conversational memory and guardrails.\n\n"
            "1. LOOKUP REQUIREMENT:\n"
            "   - ALWAYS look up a customer's profile using `get_customer_details` before performing any upgrades or modifications.\n\n"
            "2. CONTEXT TRACKING & SWAPPING:\n"
            "   - Never assume an account ID. If the user refers to 'them', 'this account', or 'him/her', review the conversation history to find the active customer ID.\n"
            "   - If no customer has been discussed yet, politely ask the user for the customer ID before running tools.\n"
            "   - If discussing one customer (e.g., CUST-101) and the user explicitly names a different account (e.g., CUST-102), immediately switch your active context to the new account.\n\n"
            "3. AMBIGUITY RESOLUTION:\n"
            "   - If the user provides a first name instead of an ID, fetch details. If multiple accounts match that name (e.g., two people named Nondumiso), DO NOT execute an upgrade tool. Stop and ask the user to clarify by listing the matching options.\n\n"
            "4. HUMAN-IN-THE-LOOP SAFETY:\n"
            "   - NEVER call `update_customer_tier` directly when a modification is first requested.\n"
            "   - First, summarize the pending change (Old Tier -> New Tier and Rate) and ask plainly: 'Would you like me to proceed with this change?'\n"
            "   - ONLY execute the tool if the user explicitly confirms with a 'yes', 'proceed', or clear validation.\n"
            "   - If they reject it or say 'no', cancel the action and summarize that no changes were made."
        ),
        tools=my_billing_tools,
        temperature=0.1
    )
)

if __name__ == "__main__":
    print("--- Interactive Billing Agent Initialized ---")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input("[User]: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Ending session. Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            response = chat.send_message(user_input)
            print(f"[Agent]: {response.text}\n")
            
        except Exception as e:
            print(f"[System Error]: {e}\n")