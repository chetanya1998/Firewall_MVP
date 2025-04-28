# simulator/Traffic_Simulator.py

import time
import random
import requests
from faker import Faker
from fake_useragent import UserAgent

fake = Faker()
ua = UserAgent()

BASE_URL = "http://127.0.0.1:5000"

# Simulated IP Blocks by Country
IP_POOLS = {
    "USA": ["3.0.0.", "13.52.0.", "18.144.0.", "34.208.0."],
    "India": ["49.205.0.", "103.25.0.", "43.224.0.", "182.72.0."],
    "Germany": ["18.194.0.", "3.120.0.", "35.157.0.", "52.58.0."],
    "Singapore": ["13.228.0.", "52.220.0.", "18.136.0.", "54.169.0."],
    "Australia": ["13.238.0.", "3.104.0.", "52.62.0.", "54.153.0."]
}

paths_human = ["/home", "/products", "/about", "/contact", "/shop", "/faq"]
paths_bot = ["/admin", "/wp-login.php", "/login", "/search", "/config", "/hidden"]

def generate_ip(country):
    """Generate a realistic IP address for a given country."""
    ip_prefix = random.choice(IP_POOLS[country])
    return ip_prefix + str(random.randint(1, 255))

def send_request(ip, user_agent, path, country):
    headers = {
        "User-Agent": user_agent,
        "X-Forwarded-For": ip,
        "X-Country": country  # Custom header (optional for logging)
    }
    try:
        requests.get(f"{BASE_URL}{path}", headers=headers, timeout=3)
        print(f"Sent {path} from {ip} ({country}) [{user_agent}]")
    except Exception as e:
        print(f"Error sending request: {e}")

def simulate_human():
    country = random.choice(list(IP_POOLS.keys()))
    ip = generate_ip(country)
    user_agent = ua.random
    session = random.sample(paths_human, random.randint(2, 5))
    for path in session:
        send_request(ip, user_agent, path, country)
        time.sleep(random.uniform(1.5, 4.0))

def simulate_bot():
    country = random.choice(list(IP_POOLS.keys()))
    ip = generate_ip(country)
    user_agent = random.choice(["ScrapyBot/2.4.1", "curl/7.64.1", "Python-urllib/3.8", "Googlebot/2.1"])
    session = random.sample(paths_bot, random.randint(2, len(paths_bot)))
    for path in session:
        send_request(ip, user_agent, path, country)
        time.sleep(random.uniform(0.2, 0.5))

def orchestrator():
    while True:
        choice = random.choices(["human", "bot"], weights=[0.6, 0.4])[0]
        if choice == "human":
            simulate_human()
        else:
            simulate_bot()
        time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    print("🚀 Traffic Simulator with Global IPs Started...")
    orchestrator()
