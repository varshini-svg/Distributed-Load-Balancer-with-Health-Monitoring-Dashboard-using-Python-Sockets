import threading


class ConnectionPool:
    def __init__(self, servers):
        """
        Initialize connection pool
        servers: list of backend servers
        """
        self.lock = threading.Lock()

        # Track active connections per server index
        self.connections = {i: 0 for i in range(len(servers))}

        # Store server info
        self.servers = servers

    # -------------------------------
    # Increment connection count
    # -------------------------------
    def increment(self, index):
        with self.lock:
            if index in self.connections:
                self.connections[index] += 1

    # -------------------------------
    # Decrement connection count
    # -------------------------------
    def decrement(self, index):
        with self.lock:
            if index in self.connections and self.connections[index] > 0:
                self.connections[index] -= 1

    # -------------------------------
    # Get least loaded server index
    # -------------------------------
    def get_least_loaded(self):
        with self.lock:
            if not self.connections:
                return None

            return min(self.connections, key=self.connections.get)

    # -------------------------------
    # Get current connection stats
    # -------------------------------
    def get_stats(self):
        with self.lock:
            return self.connections.copy()

    # -------------------------------
    # Add new server dynamically
    # -------------------------------
    def add_server(self, server):
        with self.lock:
            index = len(self.servers)
            self.servers.append(server)
            self.connections[index] = 0

    # -------------------------------
    # Remove server (e.g., if down)
    # -------------------------------
    def remove_server(self, index):
        with self.lock:
            if index in self.connections:
                del self.connections[index]

            if index < len(self.servers):
                self.servers.pop(index)

            # Rebuild index mapping (important)
            self.connections = {
                i: self.connections.get(i, 0)
                for i in range(len(self.servers))
            }

    # -------------------------------
    # Reset all connections
    # -------------------------------
    def reset(self):
        with self.lock:
            for key in self.connections:
                self.connections[key] = 0