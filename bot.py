from flask import Flask, request
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
VERIFY_TOKEN = "Satsurai#17"
PAGE_ACCESS_TOKEN = "EAAWlhZAXUmkMBRmi7U7BUjIEkRzIW6ZB0bSwgI2dqQ96oTGczFRr0eoYO2gxzZAgtEYbqJazcDygcAdu1IaSGdZAMHP2WHeR552hSZAsmRqQ7VbhbEhffYomjHnhWoHZC0PdAB3j5u0pZBdzWMZAJpgdhwUr6zt7vk3YBGeZCGaqi74tNEVSVsojcvLjaG439iJxxt4UhIVFn"

@app.route("/", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Erreur de token"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and data.get("object") == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if event.get("message") and event["message"].get("text"):
                    send_message(
                        event["sender"]["id"],
                        f"Seïkī Bot actif. Reçu : {event['message']['text']}",
                    )
    return "ok", 200

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v20.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    requests.post(url, json={"recipient": {"id": recipient_id}, "message": {"text": text}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)