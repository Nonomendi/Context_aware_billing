import os
from google import genai
from google.genai import types

from db_tools import get_customer_details, update_customer_tier

# Pull the API key dynamically from your system environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

my_billing_tools = [get_customer_details, update_customer_tier]

chat = client.chats.create(
    model='gemini-2.5-flash',
     config=types.GenerateContentConfig(
        system_instruction=(
           "You are an expert customer billing assistant with conversational memory.\n\n"
            "CRITICAL GUARDRAILS:\n"
            "1. ALWAYS look up a customer's current details using `get_customer_details` before performing an upgrade.\n"
            "2. Never assume a customer ID. If the user refers to 'them', 'this account', or 'him/her', check your conversation history "
            "3. NEVER execute the `update_customer_tier` tool unless the user has explicitly confirmed "
            "with a 'yes', 'proceed', or clear agreement after you present the cost breakdown.\n"
            "4. If the user asks to upgrade but hasn't confirmed yet, summarize the pending change "
            "(Old Tier -> New Tier and Rate) and ask them plainly: 'Would you like me to proceed with this change?'\n"
            "5. If they say no, cancel the action and do not call the update tool."
            "to find the active `customer_id` currently being discussed.\n"
            "6. If no customer has been mentioned yet in the chat history, politely ask the user for the customer ID before taking action.\n"
            "7. Clearly summarize what changes were made after a successful tool execution."
            
        ),
        tools=my_billing_tools,
        temperature=0.1
    )
)

print("--- Interactive Billing Agent Initialized ---")
# print("Type 'exit' or 'quit' to end the session.\n")

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

