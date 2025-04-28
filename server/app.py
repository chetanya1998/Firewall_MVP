# server/app.py

from flask import Flask, request
import time
import os

app = Flask(__name__)

LOG_FILE = "logs/access.log"

# Ensure logs folder exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def log_request(path):
    # Fetch IP from X-Forwarded-For header or fallback to remote_addr
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    
    # Fetch User-Agent
    user_agent = request.headers.get("User-Agent", "unknown")
    
    # Fetch Country from X-Country header (sent by simulator)
    country = request.headers.get("X-Country", "Unknown")
    
    # Log format: timestamp | ip | country | user_agent | path
    log_line = f"{time.time()} | {ip} | {country} | {user_agent} | /{path}\n"
    
    # Append to access.log
    with open(LOG_FILE, "a") as f:
        f.write(log_line)
    
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
