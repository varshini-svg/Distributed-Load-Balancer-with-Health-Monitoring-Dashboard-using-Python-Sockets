import socket
import time
from utils.constants import DEFAULT_BUFFER_SIZE


# -------------------------------
# Create TCP Socket
# -------------------------------
def create_socket(timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    return s


# -------------------------------
# Send HTTP Request
# -------------------------------
def send_http_request(host, port, request_data):
    try:
        sock = create_socket()
        sock.connect((host, port))
        sock.sendall(request_data)

        response = b""

        while True:
            try:
                chunk = sock.recv(DEFAULT_BUFFER_SIZE)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break

        sock.close()
        return response

    except Exception as e:
        return None


# -------------------------------
# Simple Health Check
# -------------------------------
def is_server_alive(host, port, timeout=2):
    try:
        sock = create_socket(timeout)
        sock.connect((host, port))
        sock.close()
        return True
    except:
        return False


# -------------------------------
# Format HTTP Response
# -------------------------------
def build_http_response(status="200 OK", body="OK"):
    response = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )
    return response.encode()


# -------------------------------
# Get Current Timestamp
# -------------------------------
def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------
# Safe Close Socket
# -------------------------------
def safe_close(sock):
    try:
        sock.close()
    except:
        pass


# -------------------------------
# Retry Wrapper
# -------------------------------
def retry_operation(func, retries=2, delay=1, *args, **kwargs):
    for attempt in range(retries):
        result = func(*args, **kwargs)
        if result:
            return result
        time.sleep(delay)
    return None


# -------------------------------
# Extract Server ID
# -------------------------------
def get_server_id(server, index=None):
    if "id" in server:
        return server["id"]
    return f"S{index}" if index is not None else "Unknown"