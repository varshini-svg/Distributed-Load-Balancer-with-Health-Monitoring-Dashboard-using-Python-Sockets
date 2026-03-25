# -------------------------------
# Network Constants
# -------------------------------
DEFAULT_HOST = "127.0.0.1"
DEFAULT_LB_PORT = 8080
DEFAULT_BUFFER_SIZE = 4096
DEFAULT_TIMEOUT = 5


# -------------------------------
# HTTP Constants
# -------------------------------
HTTP_OK = "200 OK"
HTTP_BAD_GATEWAY = "502 Bad Gateway"
HTTP_INTERNAL_ERROR = "500 Internal Server Error"

CONTENT_TYPE_TEXT = "text/plain"


# -------------------------------
# Algorithm Names
# -------------------------------
ALGO_ROUND_ROBIN = "round_robin"
ALGO_LEAST_CONNECTIONS = "least_connections"
ALGO_WEIGHTED = "weighted"


# -------------------------------
# Server Status
# -------------------------------
STATUS_UP = "UP"
STATUS_DOWN = "DOWN"


# -------------------------------
# Logging Levels (optional use)
# -------------------------------
LOG_DEBUG = "DEBUG"
LOG_INFO = "INFO"
LOG_WARNING = "WARNING"
LOG_ERROR = "ERROR"
LOG_CRITICAL = "CRITICAL"


# -------------------------------
# Dashboard Config
# -------------------------------
DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 5000
REFRESH_INTERVAL = 2  # seconds


# -------------------------------
# Retry / Health Config Defaults
# -------------------------------
DEFAULT_HEALTH_INTERVAL = 5
DEFAULT_HEALTH_TIMEOUT = 2
DEFAULT_MAX_RETRIES = 2


# -------------------------------
# Messages
# -------------------------------
MSG_NO_SERVER = "No backend servers available"
MSG_SERVER_DOWN = "Server is down"
MSG_REQUEST_FAILED = "Request forwarding failed"
MSG_SUCCESS = "Request successful"