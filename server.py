
import os
import socket
import socket

try:
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_RAW,
        socket.IPPROTO_RAW
    )
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    print("IP_HDRINCL_AVAILABLE", flush=True)
    s.close()
except Exception as e:
    print(f"IP_HDRINCL_UNAVAILABLE: {e!r}", flush=True)

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    print(f"TCP probe listening on {HOST}:{PORT}", flush=True)

    while True:
        conn, addr = server.accept()
        with conn:
            print(f"Connection from {addr}", flush=True)
            data = conn.recv(4096)
            print(f"Received: {data!r}", flush=True)
            conn.sendall(b"RAILWAY-OK\n")
