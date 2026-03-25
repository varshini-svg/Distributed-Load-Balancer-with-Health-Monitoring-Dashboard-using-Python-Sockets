import socket
import threading
import argparse
import time

# -----------------------------
# Handle each client connection
# -----------------------------
def handle_client(conn, addr, port, delay):
    try:
        print(f"[+] Connection from {addr} on port {port}")

        request = conn.recv(1024).decode()

        if not request:
            return

        print(f"[REQUEST] {addr}:\n{request.strip()}")

        # Simulate delay (for testing Least Connections)
        if delay > 0:
            time.sleep(delay)

        # Create HTTP response
        response_body = f"""
        <html>
        <body>
            <h2>Response from Backend Server</h2>
            <p>Server Port: {port}</p>
            <p>Handled Client: {addr}</p>
        </body>
        </html>
        """

        response = f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {len(response_body)}

{response_body}
"""

        conn.sendall(response.encode())

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        conn.close()
        print(f"[-] Connection closed: {addr}")


# -----------------------------
# Start server
# -----------------------------
def start_server(host, port, delay):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Reuse address (avoid restart issues)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((host, port))
    server.listen(10)

    print(f"🚀 Backend Server running on {host}:{port} (delay={delay}s)")

    while True:
        conn, addr = server.accept()

        # Handle each client in new thread
        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, port, delay)
        )
        client_thread.start()


# -----------------------------
# Main entry
# -----------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backend Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host address")
    parser.add_argument("--port", type=int, required=True, help="Port number")
    parser.add_argument("--delay", type=int, default=0, help="Response delay (seconds)")
    parser.add_argument("--id", default="Server")
    args = parser.parse_args()

    start_server(args.host, args.port, args.delay)