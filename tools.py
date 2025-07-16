from agents import function_tool
import requests
from ddgs import DDGS # This imports from pip-installed package
import os
import json

def load_data(path="data_base.json") -> list[dict]:
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return []

    try:
        with open(path, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("❌ Invalid format: Expected a list of users.")
                return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return []

users = load_data()


token = os.environ.get("TOKEN")

@function_tool
async def get_user_data(min_age: int, match_type: str) -> list[dict]:
    """
    Retrieve user data based on minimum age and match type (groom/bride)
    """
    min_age = int(min_age)
    match_type = match_type.lower()

    filtered = [user for user in users if user["gender"] == match_type and int(user["age"]) >= min_age]
    return filtered

@function_tool
async def send_whatsapp_tool(user_number: str, message: str) -> str:
    """
    Sends a WhatsApp message using Ultramsg.
    """

    try:

        url = "https://api.ultramsg.com/instance132025/messages/chat"

        payload = f"token={token}&to={user_number}&body={message}"
        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.text
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"

@function_tool
async def web_search_tool(name: str, title: str) -> dict:
    """
    Search LinkedIn profile by name and title using DuckDuckGo.
    Returns the most relevant result.
    """

    query = f"{name} {title} site:linkedin.com"
    print(f"🔍 Searching: {query}")

    with DDGS() as ddgs:
        results = ddgs.text(query)

        # Convert iterator to list
        results_list = list(results)

        if not results_list:
            return {
                "name": name,
                "title": title,
                "linkedin_profile": "Not found",
                "note": "No relevant LinkedIn profile found"
            }

        top = results_list[0]
        return {
            "name": name,
            "title": title,
            "linkedin_profile": top["href"],
            "description": top["body"]
        }
