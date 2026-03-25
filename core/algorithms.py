import threading


# -------------------------------
# Round Robin Algorithm
# -------------------------------
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers
        self.index = 0
        self.lock = threading.Lock()

    def get_server(self):
        with self.lock:
            if not self.servers:
                return None

            server = self.servers[self.index]
            self.index = (self.index + 1) % len(self.servers)

            return server


# -------------------------------
# Least Connections Algorithm
# -------------------------------
class LeastConnections:
    def __init__(self, servers):
        self.servers = servers
        self.connections = {i: 0 for i in range(len(servers))}
        self.lock = threading.Lock()

    def get_server(self):
        with self.lock:
            if not self.servers:
                return None

            # Find server with minimum connections
            index = min(self.connections, key=self.connections.get)
            self.connections[index] += 1

            return self.servers[index], index

    def release_server(self, index):
        with self.lock:
            if index in self.connections and self.connections[index] > 0:
                self.connections[index] -= 1


# -------------------------------
# Weighted Round Robin Algorithm
# -------------------------------
class WeightedRoundRobin:
    def __init__(self, servers):
        """
        Each server must have a 'weight' key
        Example:
        {"host": "127.0.0.1", "port": 9001, "weight": 2}
        """
        self.servers = []
        self.lock = threading.Lock()

        # Expand server list based on weight
        for server in servers:
            weight = server.get("weight", 1)
            for _ in range(weight):
                self.servers.append(server)

        self.index = 0

    def get_server(self):
        with self.lock:
            if not self.servers:
                return None

            server = self.servers[self.index]
            self.index = (self.index + 1) % len(self.servers)

            return server


# -------------------------------
# Factory (Optional but useful)
# -------------------------------
class AlgorithmFactory:
    @staticmethod
    def create(algorithm_name, servers):
        if algorithm_name == "round_robin":
            return RoundRobin(servers)

        elif algorithm_name == "least_connections":
            return LeastConnections(servers)

        elif algorithm_name == "weighted":
            return WeightedRoundRobin(servers)

        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")