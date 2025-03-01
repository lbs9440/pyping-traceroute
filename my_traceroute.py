import argparse
import socket
import struct
import time
import os
import select
import statistics

def calculate_checksum(data):
    """Compute the ICMP checksum
    
    :param data: data to compute the checksum
    :return checksum:
    """
    if len(data) % 2:
        data += b'\x00' 
    checksum = sum((data[i] << 8) + data[i + 1] for i in range(0, len(data), 2))
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def create_packet(identifier, seq, size):
    """Create ICMP Echo Request packet
    
    :param identifier: unique id for the packet
    :param seq: sequence number for the packet
    :param size: size of the packet in bytes
    :return: returns the packet
    """
    header = struct.pack('!BBHHH', 8, 0, 0, identifier, seq)
    payload = bytes(range(size))
    checksum = calculate_checksum(header + payload)
    header = struct.pack('!BBHHH', 8, 0, checksum, identifier, seq)
    return header + payload

def resolve_target(target):
    """Given a domain as the hostname, get the ip
    
    :param target: target destination of the packets
    :return: ip of the target
    """
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
        

def resolve_domain(ip):
    """Given an IP address, gets the host name

    :param ip: IP address
    :return: hostname/domain of the IP address
    """
    try:
        domain_name = socket.gethostbyaddr(ip)[0]
        return domain_name
    except socket.herror:
        return None  # No domain name found

def send_probe(dest, ttl, probe_count, print_numerically, timeout=4):
    """Send ICMP Echo Requests (probes) to a destination with a given TTL
    
    :param dest: target destination IP
    :param ttl: Time-To-Live value for packets
    :param probe_count: number of probes per TTL
    :param print_numerically: whether to print only numerical addresses
    :param timeout: timeout for each probe response (default: 4s)
    :return: list of probe results (address, TTL, round-trip time) or None on timeout
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
        s.settimeout(timeout)  
    except PermissionError:
        print("Permission denied: Run the script as root to use raw sockets.")
        return []

    identifier = os.getpid() & 0xFFFF
    probes = []

    for seq in range(1, probe_count + 1):
        packet = create_packet(identifier, seq, 56)
        start_time = time.time()
        s.sendto(packet, (dest, 1))
        domain_name = None

        try:
            response, addr = s.recvfrom(1024) 
            addr = addr[0]
            rtt = time.time() - start_time
            ttl_value = struct.unpack("!B", response[8:9])[0]
            probes.append((addr, ttl_value, rtt))
            if seq == 1 and domain_name is None and not print_numerically:
                domain_name = resolve_domain(addr)
            if seq == 1:
                if domain_name and not print_numerically:
                    print(f"{domain_name} ({addr})", end=" ")
                else:
                    print(f"{addr}" if print_numerically else f"{addr} ({addr})", end=" ")
                print
            print(f"{rtt * 1000:.3f} ms", end=" ")
        except socket.timeout:
            probes.append(None)  # No response received
            print("*", end=" ")

    return probes


def traceroute(dest, max_hops, probe_count, print_numerically, print_summary):
    """Perform a traceroute to a destination
    
    :param dest: target IP address
    :param max_hops: maximum number of hops to trace
    :param probe_count: number of probes per hop
    :param print_numerically: whether to print only IPs
    :param print_summary: whether to display packet loss per hop
    """
    print(f"Traceroute to {dest} ({dest}), {max_hops} hops max, 40 byte packets")

    ttl = 1
    unanswered_probes = 0
    while ttl <= max_hops:
        print(f"{ttl:2}", end=" ")

        probes = send_probe(dest, ttl, probe_count, print_numerically)

        if probes and probes[0] is None:
            unanswered_probes += probe_count
        else:
            addr = probes[0][0]  

            # Check if destination is reached
            if addr == dest:
                for probe in probes:
                    if probe is None:
                        unanswered_probes += 1
                if print_summary:
                    loss_percent = (unanswered_probes / probe_count) * 100
                    print(f"({loss_percent:.0f}% loss)", end=" ")
                unanswered_probes = 0
                print() 
                break  # Stop the traceroute

            for probe in probes:
                if probe is None:
                    unanswered_probes += 1
            
        if print_summary:
            loss_percent = (unanswered_probes / probe_count) * 100
            print(f"({loss_percent:.0f}% loss)", end=" ")
        unanswered_probes = 0          

        print()  
        ttl += 1


def main():
    parser = argparse.ArgumentParser(description="Unix-style Traceroute command")
    parser.add_argument("-n", action='store_true', help='Print hop addresses numerically')
    parser.add_argument("-q", type=int, default=3, help="Number of probes per TTL (default: 3)")
    parser.add_argument("-S", action='store_true', help="Print summary of how many probes were not answered per hop")
    parser.add_argument("host", type=str, help="Target IP or Hostname for traceroute")

    args = parser.parse_args()

    ip, hostname = resolve_target(args.host)
    if ip:
        traceroute(ip, 64, args.q, args.n, args.S)
    

if __name__ == '__main__':
    main()
