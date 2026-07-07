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
            "to find the active `customer_id` currently being discussed.\n"
            "3. If no customer has been mentioned yet in the chat history, politely ask the user for the customer ID before taking action.\n"
            "4. Clearly summarize what changes were made after a successful tool execution."
            
        ),
        tools=my_billing_tools,
        temperature=0.1
    )
)

def run_billing_agent(user_message: str):
    print(f"\n[User]: {user_message}")
    response = chat.send_message(user_message)
    print(f"[Agent]: {response.text}")

if __name__ == "__main__":
    print("--- Starting Phase 3 Agent Testing ---")
    run_billing_agent("Can you look into the account for customer CUST-101.")
    run_billing_agent("Please upgrade them to the Premium tier at R350.00 per month.")