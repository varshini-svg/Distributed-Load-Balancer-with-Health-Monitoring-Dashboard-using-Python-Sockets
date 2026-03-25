import socket
from core.logger import get_logger

logger = get_logger("RequestHandler")


# -------------------------------
# Parse HTTP Request (Basic)
# -------------------------------
def parse_request(data):
    try:
        request_text = data.decode(errors="ignore")
        lines = request_text.split("\r\n")

        request_line = lines[0] if lines else ""
        method, path, version = ("", "", "")

        if request_line:
            parts = request_line.split()
            if len(parts) == 3:
                method, path, version = parts

        headers = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value

        return {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers,
            "raw": data
        }

    except Exception as e:
        logger.error(f"Request parsing failed: {e}")
        return None


# -------------------------------
# Forward request to backend
# -------------------------------
def forward_request(server, request_data, timeout=5):
    try:
        backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend.settimeout(timeout)

        backend.connect((server["host"], server["port"]))
        backend.sendall(request_data)

        response = b""

        while True:
            try:
                chunk = backend.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break

        backend.close()
        return response

    except Exception as e:
        logger.error(f"Forwarding failed to {server}: {e}")
        return None


# -------------------------------
# Retry mechanism (failover)
# -------------------------------
def forward_with_retry(servers, request_data, retries=2):
    for attempt in range(retries):
        for server in servers:
            logger.info(f"Trying server {server}")

            response = forward_request(server, request_data)

            if response:
                logger.info(f"Success from {server}")
                return response

            logger.warning(f"Failed attempt on {server}")

        logger.warning(f"Retry attempt {attempt + 1} failed")

    logger.error("All retries failed")
    return None


# -------------------------------
# Handle client request end-to-end
# -------------------------------
def handle_request(client_conn, servers):
    try:
        request_data = client_conn.recv(4096)

        if not request_data:
            client_conn.close()
            return

        parsed = parse_request(request_data)

        if parsed:
            logger.info(f"{parsed['method']} {parsed['path']}")

        # Try forwarding with retry mechanism
        response = forward_with_retry(servers, request_data)

        if response:
            client_conn.sendall(response)
        else:
            send_error(client_conn, 502, "Bad Gateway")

    except Exception as e:
        logger.error(f"Request handling error: {e}")

    finally:
        client_conn.close()


# -------------------------------
# Send error response to client
# -------------------------------
def send_error(conn, code, message):
    body = f"{code} {message}\n"

    response = (
        f"HTTP/1.1 {code} {message}\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
        f"{body}"
    )

    try:
        conn.sendall(response.encode())
    except:
        pass