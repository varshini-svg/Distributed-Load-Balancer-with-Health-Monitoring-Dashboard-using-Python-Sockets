import json
import os


# -------------------------------
# Base Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

SERVERS_FILE = os.path.join(CONFIG_DIR, "servers.json")


# -------------------------------
# Load Servers from JSON
# -------------------------------
def load_servers():
    try:
        with open(SERVERS_FILE, "r") as f:
            data = json.load(f)
            return data.get("servers", [])
    except Exception as e:
        print(f"[Settings] Error loading servers.json: {e}")
        return []


# -------------------------------
# Global Configurations
# -------------------------------
SERVERS = load_servers()

# Load Balancer Config
LB_HOST = "127.0.0.1"
LB_PORT = 8080

# Algorithm Selection
# Options: "round_robin", "least_connections", "weighted"
ALGORITHM = "round_robin"

# Health Checker Config
HEALTH_CHECK_INTERVAL = 5      # seconds
HEALTH_CHECK_TIMEOUT = 2       # seconds

# Retry Config
MAX_RETRIES = 2

# Logging Config
LOG_LEVEL = "DEBUG"


# -------------------------------
# Reload Servers (Optional Feature)
# -------------------------------
def reload_servers():
    global SERVERS
    SERVERS = load_servers()
    print("[Settings] Servers reloaded")


# -------------------------------
# Utility: Get Active Server List
# -------------------------------
def get_servers():
    return SERVERS.copy()