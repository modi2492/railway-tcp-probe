
import socket
import struct

DST = "162.35.32.29"
SRC = "0.0.0.0"
SPORT = 40123
DPORT = 18081
PAYLOAD = b"RAILWAY-RAW-001"

def checksum(data):
    if len(data) % 2:
        data += b"\0"
    words = struct.unpack("!" + "H" * (len(data) // 2), data)
    total = sum(words)
    while total >> 16:
        total = (total & 0xffff) + (total >> 16)
    return (~total) & 0xffff

try:
    tcp = struct.pack(
        "!HHIIHHHH",
        SPORT, DPORT, 0x12345678, 0,
        (5 << 12) | 0x02, 64240, 0, 0
    )
    pseudo = (
        socket.inet_aton(SRC)
        + socket.inet_aton(DST)
        + b"\0\x06"
        + struct.pack("!H", len(tcp) + len(PAYLOAD))
    )
    tcp = tcp[:16] + struct.pack(
        "!H", checksum(pseudo + tcp + PAYLOAD)
    ) + tcp[18:]

    total = 20 + len(tcp) + len(PAYLOAD)
    ip = struct.pack(
        "!BBHHHBBH4s4s",
        0x45, 0, total, 0x4567, 0, 64, 6, 0,
        socket.inet_aton(SRC), socket.inet_aton(DST)
    )
    ip = ip[:10] + struct.pack("!H", checksum(ip)) + ip[12:]

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    print("sendto:", s.sendto(ip + tcp + PAYLOAD, (DST, DPORT)), flush=True)
    s.close()
except Exception as e:
    print("RAW_SEND_ERROR:", repr(e), flush=True)
