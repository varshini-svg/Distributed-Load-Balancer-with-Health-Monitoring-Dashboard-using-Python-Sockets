import socket
import threading
import argparse
import time
import random

# -------------------------------
# Handle client connection
# -------------------------------
def handle_client(conn, addr, server_id, min_delay, max_delay):
    try:
        print(f"[{server_id}] Connected by {addr}")

        request = conn.recv(1024).decode()

        if not request:
            conn.close()
            return

        print(f"[{server_id}] Request received")

        # Simulate variable delay (slow response)
        delay = random.uniform(min_delay, max_delay)
        print(f"[{server_id}] Processing with delay: {delay:.2f}s")
        time.sleep(delay)

        # Create HTTP response
        response_body = (
            f"⚠️ Slow response from Server {server_id}\n"
            f"Delay: {delay:.2f} seconds\n"
        )

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "\r\n"
            f"{response_body}"
        )

        conn.sendall(response.encode())

    except Exception as e:
        print(f"[{server_id}] Error: {e}")

    finally:
        conn.close()
        print(f"[{server_id}] Connection closed: {addr}")


# -------------------------------
# Start slow server
# -------------------------------
def start_server(host, port, server_id, min_delay, max_delay):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow reuse of address
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((host, port))
    server.listen(10)

    print(f"[{server_id}] Slow Server running on {host}:{port}")
    print(f"[{server_id}] Delay range: {min_delay}s - {max_delay}s")

    while True:
        conn, addr = server.accept()

        # Multi-client handling
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, server_id, min_delay, max_delay)
        )
        client_thread.daemon = True
        client_thread.start()


# -------------------------------
# Main Entry
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slow Backend Server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--id", default="SlowServer")
    parser.add_argument("--min-delay", type=float, default=1.0,
                        help="Minimum delay (seconds)")
    parser.add_argument("--max-delay", type=float, default=5.0,
                        help="Maximum delay (seconds)")

    args = parser.parse_args()

    start_server(
        args.host,
        args.port,
        args.id,
        args.min_delay,
        args.max_delay
    )