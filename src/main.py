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
            "You are an expert customer billing and account upgrade assistant. "
            "You have access to tools that can fetch customer details and update their subscription tiers. "
            "Always check customer details before making an update, and confirm actions clearly."
        ),
        tools=my_billing_tools,
    )
)

def run_billing_agent(user_message: str):
    print(f"\n[User]: {user_message}")
    response = chat.send_message(user_message)
    print(f"[Agent]: {response.text}")

if __name__ == "__main__":
    print("--- Starting Phase 2 Agent Testing ---")
    run_billing_agent("Can you look into the account for customer CUST-101 and tell me their status?")
    run_billing_agent("Please upgrade customer CUST-101 to the Premium tier at R350.00 per month.")