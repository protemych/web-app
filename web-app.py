import os
from klein import Klein
import requests
import random

app = Klein()
TOKEN_FILE = "tokens.txt"
TELEGRAM_BOT_URL = "https://t.me/"

def load_tokens():
    try:
        with open(TOKEN_FILE, "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
        return tokens
    except FileNotFoundError:
        return []

def check_bot(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)
    return response.status_code == 200

@app.route("/")
def redirect_to_bot(request):
    tokens = load_tokens()
    random.shuffle(tokens)

    for token in tokens:
        if check_bot(token):
            bot_info = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()
            bot_username = bot_info.get("result", {}).get("username")
            if bot_username:
                return f"<html><head><meta http-equiv='refresh' content='0; url={TELEGRAM_BOT_URL}{bot_username}' /></head></html>"

    return "Нет доступных ботов", 503

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Берём порт из Render
    app.run("0.0.0.0", port)
