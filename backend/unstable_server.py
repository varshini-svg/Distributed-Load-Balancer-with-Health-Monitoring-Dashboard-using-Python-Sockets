import socket
import threading
import argparse
import random
import time
import sys

# -------------------------------
# Handle client connection
# -------------------------------
def handle_client(conn, addr, server_id, fail_rate, crash_rate):
    try:
        print(f"[{server_id}] Connected by {addr}")

        request = conn.recv(1024)

        if not request:
            conn.close()
            return

        # Simulate random failure (drop request)
        if random.random() < fail_rate:
            print(f"[{server_id}] ⚠️ Dropping request (simulated failure)")
            conn.close()
            return

        # Simulate random crash
        if random.random() < crash_rate:
            print(f"[{server_id}] 💥 Server crashing!")
            conn.close()
            sys.exit(1)

        # Simulate random delay (unstable performance)
        delay = random.uniform(0.5, 3.0)
        time.sleep(delay)

        # Send HTTP response
        response_body = (
            f"⚠️ Unstable Server {server_id}\n"
            f"Response delay: {delay:.2f}s\n"
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
# Start unstable server
# -------------------------------
def start_server(host, port, server_id, fail_rate, crash_rate):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow reuse
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((host, port))
    server.listen(10)

    print(f"[{server_id}] ⚠️ Unstable Server running on {host}:{port}")
    print(f"[{server_id}] Fail rate: {fail_rate}, Crash rate: {crash_rate}")

    while True:
        try:
            conn, addr = server.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, server_id, fail_rate, crash_rate)
            )
            client_thread.daemon = True
            client_thread.start()

        except Exception as e:
            print(f"[{server_id}] Critical Error: {e}")
            break


# -------------------------------
# Main Entry
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unstable Backend Server")

    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--id", default="UNSTABLE")

    parser.add_argument("--fail-rate", type=float, default=0.3,
                        help="Probability of dropping request (0-1)")
    parser.add_argument("--crash-rate", type=float, default=0.1,
                        help="Probability of server crash (0-1)")

    args = parser.parse_args()

    start_server(
        args.host,
        args.port,
        args.id,
        args.fail_rate,
        args.crash_rate
    )