import socket
import threading
import time


class HealthChecker:
    def __init__(self, servers, interval=5, timeout=2):
        """
        servers: shared list of backend servers
        interval: time between checks (seconds)
        timeout: connection timeout
        """
        self.servers = servers
        self.interval = interval
        self.timeout = timeout

        self.lock = threading.Lock()
        self.active_servers = servers.copy()

        self.running = False

    # -------------------------------
    # Check if server is alive
    # -------------------------------
    def is_server_alive(self, server):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((server["host"], server["port"]))
            sock.close()
            return True
        except:
            return False

    # -------------------------------
    # Perform health check cycle
    # -------------------------------
    def check_servers(self):
        while self.running:
            new_active = []

            print("\n[HealthChecker] Checking servers...")

            for server in self.servers:
                alive = self.is_server_alive(server)

                if alive:
                    print(f"[HealthChecker] ✅ UP: {server}")
                    new_active.append(server)
                else:
                    print(f"[HealthChecker] ❌ DOWN: {server}")

            # Update active servers safely
            with self.lock:
                self.active_servers = new_active

            time.sleep(self.interval)

    # -------------------------------
    # Start health checker thread
    # -------------------------------
    def start(self):
        self.running = True
        thread = threading.Thread(target=self.check_servers)
        thread.daemon = True
        thread.start()

    # -------------------------------
    # Stop health checker
    # -------------------------------
    def stop(self):
        self.running = False

    # -------------------------------
    # Get active servers
    # -------------------------------
    def get_active_servers(self):
        with self.lock:
            return self.active_servers.copy()