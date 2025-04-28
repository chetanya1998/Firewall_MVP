# firewall/actions.py

import os

# Log file path
BLOCKED_IPS_LOG = "logs/blocked_ips.log"

# Memory cache to keep track of already blocked IPs
blocked_ips_memory = set()

# Ensure logs folder exists
os.makedirs(os.path.dirname(BLOCKED_IPS_LOG), exist_ok=True)

# Load already blocked IPs at startup (optional)
if os.path.exists(BLOCKED_IPS_LOG):
    with open(BLOCKED_IPS_LOG, "r") as f:
        for line in f:
            ip = line.strip()
            if ip:
                blocked_ips_memory.add(ip)

def block_ip(ip):
    """Simulate blocking an IP address and log it if not already blocked."""
    if ip in blocked_ips_memory:
        print(f"⚠️ IP {ip} is already blocked. Skipping...")
        return

    # Simulated blocking (for Mac)
    print(f"🚫 Blocking (simulated) IP: {ip}")

    # Add to memory
    blocked_ips_memory.add(ip)

    # Log to file
    with open(BLOCKED_IPS_LOG, "a") as f:
        f.write(f"{ip}\n")
