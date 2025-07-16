# 💃 Rishty Wali Aunty – AI Matchmaking Assistant 🤵‍♂️

**Rishty Wali Aunty** is a fun and culturally flavored AI assistant that helps users find perfect rishtas (matches) — just like a real-life Pakistani aunty!  
It uses OpenAI Agent SDK, web search tools, and WhatsApp integration to deliver a smart, conversational matchmaking experience.

## ✨ Features

- 🔍 Find **Grooms or Brides** based on user preferences and age
- 🌐 Fetch **LinkedIn profile details** using web search (DuckDuckGo or CSE)
- 💬 **Conversational UI** powered by Streamlit for a natural chat-like flow
- 📲 Send match summaries to **WhatsApp** using UltraMsg API
- 💾 Save **search history** locally for the last 10 rishtas
- ❤️ AI responds in a warm, aunty-style tone with cultural humor

## 🛠️ Tech Stack

- Python + Streamlit
- OpenAI Agent SDK
- DuckDuckGo Search / Google CSE API
- UltraMsg (WhatsApp API)
- JSON file storage (for mock DB + history)

## 📁 Project Structure

.
├── main.py # Streamlit app with UI + chat
├── tools.py # Agent function_tools: search, send, match
├── config.py # Your OpenAI config/token setup
├── data_base.json # Groom and bride mock database
├── history.json # Saved recent search history
├── requirements.txt # Dependencies


## 🚀 How to Run Locally

1. **Clone the repo**

```bash
git clone https://github.com/your-username/rishty-wali-aunty.git
cd rishty-wali-aunty
```
3. **Install dependencies**
```bash
pip install -r requirements.txt
```
3. **Run Streamlit app**

```bash
streamlit run main.py
```
⚙️ Configure
🔑 config.py
Set your OpenAI API key and model details in config.py.

📲 WhatsApp Setup (UltraMsg)
Replace the number and token inside send_whatsapp_tool() with your own UltraMsg credentials.

Note: Sandbox number only sends to pre-verified numbers. For full functionality, upgrade or use 360Dialog/WhatsApp Business API.



🧠 Future Ideas
- 🎭 Add profile photos with mock image URLs

- 🧑‍🤝‍🧑 Let users choose from shortlisted profiles

- 🛠️ Admin panel to update DB (add new rishtas)

- 🔐 Deploy securely with user login + database

- 🙌 Credits

Built with love 💖 and laughter 😄 by Ghulam Akber
Inspired by all the aunties working overtime to find us a good rishta!

📢 License
MIT License – Free to use, remix, or laugh at 😁


