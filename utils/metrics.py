import threading
import time


class Metrics:
    def __init__(self):
        self.lock = threading.Lock()

        # -------------------------------
        # Counters
        # -------------------------------
        self.total_requests = 0
        self.failed_requests = 0

        # -------------------------------
        # Connection tracking
        # -------------------------------
        self.active_connections = 0

        # -------------------------------
        # Per-server metrics
        # -------------------------------
        self.server_stats = {}  # {server_id: {requests, failures}}

        # -------------------------------
        # Timing metrics
        # -------------------------------
        self.response_times = []

    # -------------------------------
    # Request Tracking
    # -------------------------------
    def increment_requests(self):
        with self.lock:
            self.total_requests += 1

    def increment_failures(self):
        with self.lock:
            self.failed_requests += 1

    # -------------------------------
    # Connection Tracking
    # -------------------------------
    def increment_connections(self):
        with self.lock:
            self.active_connections += 1

    def decrement_connections(self):
        with self.lock:
            if self.active_connections > 0:
                self.active_connections -= 1

    # -------------------------------
    # Per Server Stats
    # -------------------------------
    def record_server_request(self, server_id):
        with self.lock:
            if server_id not in self.server_stats:
                self.server_stats[server_id] = {
                    "requests": 0,
                    "failures": 0
                }

            self.server_stats[server_id]["requests"] += 1

    def record_server_failure(self, server_id):
        with self.lock:
            if server_id not in self.server_stats:
                self.server_stats[server_id] = {
                    "requests": 0,
                    "failures": 0
                }

            self.server_stats[server_id]["failures"] += 1

    # -------------------------------
    # Response Time Tracking
    # -------------------------------
    def record_response_time(self, start_time):
        with self.lock:
            duration = time.time() - start_time
            self.response_times.append(duration)

            # Keep only last 100 values
            if len(self.response_times) > 100:
                self.response_times.pop(0)

    def get_avg_response_time(self):
        with self.lock:
            if not self.response_times:
                return 0
            return sum(self.response_times) / len(self.response_times)

    # -------------------------------
    # Get Metrics Snapshot
    # -------------------------------
    def get_metrics(self):
        with self.lock:
            return {
                "total_requests": self.total_requests,
                "failed_requests": self.failed_requests,
                "active_connections": self.active_connections,
                "avg_response_time": round(self.get_avg_response_time(), 4),
                "server_stats": self.server_stats.copy()
            }


# -------------------------------
# Global Metrics Instance
# -------------------------------
metrics = Metrics()