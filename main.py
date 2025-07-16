import streamlit as st
import asyncio
import json
import os
from datetime import datetime
from agents import Agent, Runner
from config import config
from tools import get_user_data, web_search_tool, send_whatsapp_tool

# --- Session State Initialization ---
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# --- History Management ---
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Aunty couldn’t load history: {e}")
            return []
    return []

def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history[:10], f, indent=2)
    except Exception as e:
        st.error(f"Aunty couldn’t save history: {e}")

# --- Agent Logic ---
async def run_agent(prompt: str) -> str:
    agent = Agent(
        name="Rishty Wali Aunty",
        instructions="""
        You are Rishty Wali Aunty, a warm and friendly matchmaker who speaks in a conversational, aunty-like tone (e.g., "Beta, let me find you a perfect match!"). 
        Your job is to find suitable matches based on user preferences.
        Use get_user_data to fetch initial match details, then use web_search_tool to gather LinkedIn profiles.
        Present 2-3 matches in a friendly, summarized format (e.g., name, age, profession, city, linkedin profile). After presenting, inform the user that the same data has also been sent to WhatsApp (if number is provided).
        Always repeat the full match summary in the UI response so the user can view it even if WhatsApp fails.
        Keep responses concise, warm, and culturally appropriate, like a Pakistani aunty would.
        If no matches are found, suggest tweaking preferences and ask for more details.
        """,
        tools=[get_user_data, web_search_tool, send_whatsapp_tool]
    )
    try:
        result = await Runner.run(
            starting_agent=agent,
            input=prompt,
            run_config=config
        )
        return result.final_output
    except Exception as e:
        return f"Sorry, beta! Aunty hit a snag: {e}"

# --- Streamlit App ---
async def main():
    st.set_page_config(page_title="Rishty Wali Aunty", page_icon="💍", layout="centered")

    # --- Header ---
    st.title("💃 Rishty Wali Aunty 🤵‍♂️")
    st.markdown("**Beta, let Aunty find you a perfect rishta!** Just tell me what you're looking for, and I'll do the rest. 😊")

    # --- Chat Container Placeholder ---
    response_placeholder = st.empty()

    # --- Input Form ---
    with st.form("rishta_form"):
        st.markdown("### Tell Aunty Your Preferences")
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Minimum Age", min_value=18, max_value=100, value=25, help="Aunty will find someone this age or older.")
        with col2:
            match_type = st.selectbox("Looking for", ["Groom", "Bride"], help="Who are we searching for, beta?")

        whatsapp_number = st.text_input("Your WhatsApp Number (optional)", placeholder="+923001234567", help="Aunty can send match details here!")
        user_preferences = st.text_area(
            "💬 Additional Preferences (optional)",
            placeholder="E.g., 'Someone from Lahore, loves cooking, works in tech...'",
            help="Tell Aunty any special details you want in your match!"
        )
        submitted = st.form_submit_button("🔍 Find My Rishta!")

    if submitted:
        if whatsapp_number and not whatsapp_number.startswith("+92"):
            st.warning("Beta, please enter a valid Pakistani number starting with +92!")
        else:
            prompt = f"""
            Find a {match_type.lower()} aged {min_age} or more. 
            Preferences: {user_preferences or 'None provided'}.
            WhatsApp: {whatsapp_number or 'Not provided'}.
            """
            with st.spinner("Aunty is searching for the perfect rishta... 💫"):
                response = await run_agent(prompt)
                st.session_state.conversation.append({"role": "user", "content": "I want a rishta! " + prompt})
                st.session_state.conversation.append({"role": "assistant", "content": response})

                # Save to history
                save_history({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "match_type": match_type,
                    "min_age": min_age,
                    "preferences": user_preferences or "None",
                    "whatsapp": whatsapp_number or "Not provided",
                    "output": response
                })

                # Show response below the form
                with response_placeholder.container():
                    st.markdown("### 🧕 Aunty's Rishta Summary")
                    st.markdown(response)

    # --- Chat UI Below Everything ---
    if st.session_state.conversation:
        st.markdown("---")
        st.markdown("### 🧕 Aunty's Rishta Chat History")
        for msg in st.session_state.conversation:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

if __name__ == "__main__":
    asyncio.run(main())
