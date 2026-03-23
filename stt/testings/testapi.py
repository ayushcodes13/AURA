import requests, os
from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env")

KEY = os.getenv("DEEPGRAM_API_KEY")

print("KEY:", KEY)

r = requests.get(
    "https://api.deepgram.com/v1/projects",
    headers={"Authorization": f"Token {KEY}"}
)

print("STATUS:", r.status_code)
print("BODY:", r.text)