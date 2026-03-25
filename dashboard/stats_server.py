from flask import Flask, jsonify, render_template
from config.settings import SERVERS
from core.connection_pool import ConnectionPool
from core.health_checker import HealthChecker

# -------------------------------
# Initialize Flask App
# -------------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# -------------------------------
# Initialize Shared Components
# -------------------------------
connection_pool = ConnectionPool(SERVERS)
health_checker = HealthChecker(SERVERS)

health_checker.start()

# Global stats
total_requests = 0


# -------------------------------
# Update Request Count (Hook)
# -------------------------------
def increment_requests():
    global total_requests
    total_requests += 1


# -------------------------------
# Get Server Status Data
# -------------------------------
def get_server_data():
    active_servers = health_checker.get_active_servers()
    connection_stats = connection_pool.get_stats()

    server_data = []

    for i, server in enumerate(SERVERS):
        status = "UP" if server in active_servers else "DOWN"
        connections = connection_stats.get(i, 0)

        server_data.append({
            "id": server.get("id", f"S{i}"),
            "host": server["host"],
            "port": server["port"],
            "status": status,
            "connections": connections
        })

    return server_data


# -------------------------------
# Routes
# -------------------------------

# Dashboard UI
@app.route("/")
def dashboard():
    return render_template("index.html")


# API: Stats Data
@app.route("/stats")
def stats():
    server_data = get_server_data()

    active_servers = [s for s in server_data if s["status"] == "UP"]

    return jsonify({
        "total_requests": total_requests,
        "active_connections": sum(s["connections"] for s in server_data),
        "servers_up": len(active_servers),
        "servers": server_data
    })


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    print("📊 Dashboard running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)