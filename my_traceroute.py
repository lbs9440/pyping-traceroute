import argparse
import socket
import struct
import time
import os
import select
import statistics

def calculate_checksum(data):
    """Compute the ICMP checksum"""
    if len(data) % 2:
        data += b'\x00'  # Padding if odd-length
    checksum = sum((data[i] << 8) + data[i + 1] for i in range(0, len(data), 2))
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def create_packet(identifier, seq, size):
    """Create ICMP Echo Request packet"""
    header = struct.pack('!BBHHH', 8, 0, 0, identifier, seq)
    payload = bytes(range(size))
    checksum = calculate_checksum(header + payload)
    header = struct.pack('!BBHHH', 8, 0, checksum, identifier, seq)
    return header + payload

def resolve_target(target):
    try:
        socket.inet_aton(target)
        return target, None  
    except socket.error:
        try:
            ip = socket.gethostbyname(target)
            return ip, target
        except socket.gaierror:
            print(f"ping: {target}: Name or service not known")
            return None, None
        
def traceroute(dest, max_hops=30, timeout=2):


def main():
    parser = argparse.ArgumentParser(description="Unix-style Ping")
    parser.add_argument("host", type=str, help="Target IP or Hostname for traceroute")
    parser.add_argument("-n", action='store_true', help='Print hop addresses numerially')
    parser.add_argument("-q", type=int, default=3, help="Number of probes per TTL (default: 3)")
    parser.add_argument("-S", action='store_true', help="Print summary of how many probes were not answered per hop")

    args = parser.parse_args()
    

if __name__ == '__main__':
    main()