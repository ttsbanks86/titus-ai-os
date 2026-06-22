#!/usr/bin/env python3
"""Simple Telegram bot — tests that the bot can respond"""
import urllib.request, json, time, os

TOKEN = "***REMOVED***"
API = f"https://api.telegram.org/bot{TOKEN}"
last_update = 0

def send(chat_id, text):
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    urllib.request.urlopen(urllib.request.Request(f"{API}/sendMessage", data, {"Content-Type":"application/json"}))

def get_updates():
    global last_update
    url = f"{API}/getUpdates?offset={last_update + 1}&timeout=30"
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read())
    for update in data.get("result", []):
        last_update = update["update_id"]
        msg = update.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        text = msg.get("text", "")
        name = msg.get("from", {}).get("first_name", "User")
        if text and chat_id:
            print(f"  Received from {name}: {text}")
            reply = f"Hello {name}! I'm alive. You said: {text}"
            send(chat_id, reply)
            print(f"  Replied: {reply[:50]}...")
    return len(data.get("result", []))

print("🤖 Bankshez_bot — Simple Test Mode")
print("Send a message to @Bankshez_bot on Telegram")
print("Press Ctrl+C to stop\n")

while True:
    try:
        updates = get_updates()
        time.sleep(1)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"  Error: {e}")
        time.sleep(3)
