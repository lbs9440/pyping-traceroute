import argparse
import socket
import struct
import time
import os
import select
import statistics

def send_probe(dest, ttl, probe_count, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        s.settimeout(timeout)  # Set timeout to prevent indefinite blocking
    except PermissionError:
        print("Permission denied: Run the script as root to use raw sockets.")
        return []

    identifier = os.getpid() & 0xFFFF
    probes = []

    for seq in range(1, probe_count + 1):
        packet = create_packet(identifier, seq, 56)
        s.sendto(packet, (dest, 1))

        try:
            response, addr = s.recvfrom(1024)  # Wait for response, with timeout
            ttl_value = struct.unpack("!B", response[8:9])[0]
            probes.append((addr[0], ttl_value))
        except socket.timeout:
            probes.append(None)  # Timeout, no response received
    
    return probes

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
        
def traceroute(dest, max_hops, probe_count, print_numerically, print_summary):
    print(f"Tracerouting to {dest}...")

    ttl = 1
    unanswered_probes = 0
    total_probes = 0

    while ttl <= max_hops:
        print(f"\nHop {ttl}: ", end="")

        probes = send_probe(dest, ttl, probe_count)

        if probes:
            for probe in probes:
                if probe is None:
                    print("*", end=" ")
                    unanswered_probes += 1
                else:
                    if print_numerically:
                        print(probe[0], end=" ")
                    else:
                        print(f"{probe[0]}", end=" ")
                    
                    if probe[0] == dest:
                        print(f"{probe[0]}", end=" ")
                        return
            total_probes += probe_count
        else:
            print("No response from host")
        
        ttl += 1
    
    if print_summary:
        print(f"\n\nSummary: {unanswered_probes} probes unanswered out of {total_probes} probes")
                


def main():
    parser = argparse.ArgumentParser(description="Unix-style Traceroute command")
    parser.add_argument("-n", action='store_true', help='Print hop addresses numerically')
    parser.add_argument("-q", type=int, default=3, help="Number of probes per TTL (default: 3)")
    parser.add_argument("-S", action='store_true', help="Print summary of how many probes were not answered per hop")
    parser.add_argument("host", type=str, help="Target IP or Hostname for traceroute")

    args = parser.parse_args()

    ip, hostname = resolve_target(args.host)
    if ip:
        traceroute(ip, 30, args.q, args.n, args.S)
    

if __name__ == '__main__':
    main()
