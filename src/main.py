import os
import streamlit as str_ui
from google import genai
from google.genai import types
from dotenv import load_dotenv
from db_tools import get_customer_details, update_customer_tier

load_dotenv()

# Initialize Page Settings for the Web Browser Window
str_ui.set_page_config(page_title="Context-Aware Billing Agent", page_icon="⚡", layout="centered")
str_ui.title("⚡ Context-Aware Billing Agent")
str_ui.caption("Autonomous Customer Billing Assistant with Human-in-the-Loop Guardrails")

@str_ui.cache_resource
def get_gemini_client():
    GEMINI_API_KEY = str_ui.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=GEMINI_API_KEY)

client = get_gemini_client()
my_billing_tools = [get_customer_details, update_customer_tier]

if "gemini_chat" not in str_ui.session_state:
    str_ui.session_state.gemini_chat = client.chats.create(
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
                "   - First, summarize the pending change (Old Tier -> New Tier and Rate formatted clearly in South African Rands, e.g., R 99.00) and ask plainly: 'Would you like me to proceed with this change?'\n"
                "   - ONLY execute the tool if the user explicitly confirms with a 'yes', 'proceed', or clear validation.\n"
                "   - If they reject it or say 'no', cancel the action and summarize that no changes were made."
            ),
            tools=my_billing_tools,
            temperature=0.1
        )
    )

if "messages" not in str_ui.session_state:
    str_ui.session_state.messages = []

for msg in str_ui.session_state.messages:
    with str_ui.chat_message(msg["role"]):
        str_ui.markdown(msg["content"])

if user_prompt := str_ui.chat_input("Ask about an account or request a subscription tier update..."):
    str_ui.session_state.messages.append({"role": "user", "content": user_prompt})
    with str_ui.chat_message("user"):
        str_ui.markdown(user_prompt)
        
    with str_ui.chat_message("assistant"):
        try:
            response = str_ui.session_state.gemini_chat.send_message(user_prompt)
            agent_text = response.text
            str_ui.markdown(agent_text)
            str_ui.session_state.messages.append({"role": "assistant", "content": agent_text})
        except Exception as e:
            error_msg = f"System Error: {str(e)}"
            str_ui.error(error_msg)