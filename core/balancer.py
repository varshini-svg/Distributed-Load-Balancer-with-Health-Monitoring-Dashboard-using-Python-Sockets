import socket
import threading

from config.settings import (
    LB_HOST,
    LB_PORT,
    SERVERS,
    ALGORITHM,
    MAX_RETRIES
)

from core.algorithms import (
    RoundRobin,
    LeastConnections,
    WeightedRoundRobin
)

from core.connection_pool import ConnectionPool
from core.health_checker import HealthChecker
from core.request_handler import handle_request
from core.logger import get_logger

# Dashboard integration (optional but recommended)
try:
    from dashboard.stats_server import increment_requests
except:
    def increment_requests():
        pass


# -------------------------------
# Initialize Logger
# -------------------------------
logger = get_logger("LoadBalancer")

# -------------------------------
# Initialize Components
# -------------------------------
connection_pool = ConnectionPool(SERVERS)
health_checker = HealthChecker(SERVERS)
health_checker.start()

# Select algorithm
if ALGORITHM == "round_robin":
    algorithm = RoundRobin(SERVERS)
elif ALGORITHM == "least_connections":
    algorithm = LeastConnections(SERVERS)
elif ALGORITHM == "weighted":
    algorithm = WeightedRoundRobin(SERVERS)
else:
    raise ValueError("Invalid algorithm in settings")


# -------------------------------
# Handle each client
# -------------------------------
def handle_client(client_conn, client_addr):
    try:
        logger.info(f"Client connected: {client_addr}")
        # Get active servers
        active_servers = health_checker.get_active_servers()

        if not active_servers:
            logger.error("No active backend servers available")
            client_conn.close()
            return

        # Update algorithm server list dynamically
        algorithm.servers = active_servers

        # Increment request counter (dashboard)
        increment_requests()

        # -------------------------------
        # Round Robin / Weighted
        # -------------------------------
        if ALGORITHM in ["round_robin", "weighted"]:
            server = algorithm.get_server()

            if not server:
                logger.error("No server selected")
                client_conn.close()
                return

            handle_request(client_conn, [server])

        # -------------------------------
        # Least Connections
        # -------------------------------
        elif ALGORITHM == "least_connections":
            server, index = algorithm.get_server()

            if server is None:
                logger.error("No server selected")
                client_conn.close()
                return

            # Track connection
            connection_pool.increment(index)

            try:
                handle_request(client_conn, [server])
            finally:
                connection_pool.decrement(index)
                algorithm.release_server(index)

    except Exception as e:
        logger.error(f"Error handling client {client_addr}: {e}")

    finally:
        client_conn.close()
        logger.info(f"Client disconnected: {client_addr}")


# -------------------------------
# Start Load Balancer
# -------------------------------
def start_load_balancer():
    lb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    lb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    lb.bind((LB_HOST, LB_PORT))
    lb.listen(100)

    logger.info(f"Load Balancer running on {LB_HOST}:{LB_PORT}")
    logger.info(f"Algorithm: {ALGORITHM}")

    while True:
        try:
            client_conn, client_addr = lb.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client_conn, client_addr)
            )
            thread.daemon = True
            thread.start()

        except Exception as e:
            logger.error(f"Error accepting connection: {e}")


# -------------------------------
# Main Entry
# -------------------------------
if __name__ == "__main__":
    start_load_balancer()