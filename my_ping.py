import argparse
import socket
import struct
import time
import os
import statistics

def calculate_checksum(data):
    """Compute the ICMP checksum
    
    :param data: data to compute the checksum
    :return checksum:
    """
    if len(data) % 2:
        data += b'\x00'  # Padding if odd-length
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

def send_ping(dest_ip, count, interval, size, timeout, hostname):
    """Send ICMP Echo Request packets and display response details.
    
    :param dest_ip: Destination IP address to send the ping.
    :param count: Number of packets to send (None for unlimited).
    :param interval: Time interval between successive packets in seconds.
    :param size: Size of the ICMP payload in bytes.
    :param timeout: Time in seconds to wait for a response before considering a packet lost.
    :param hostname: Hostname of the target (if resolved from a domain).
    :return: None
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        s.settimeout(10)
    except PermissionError:
        print("ping: Operation not allowed")
        return
    
    identifier = os.getpid() & 0xFFFF
    sent, received = 0, 0
    rtt_list = []
    start_time = time.time()

    print(f"PING {hostname or dest_ip} ({dest_ip}) {size} bytes of data.")

    seq = 1

    try:
        while (count is None or seq <= count) and (timeout is None or timeout >= time.time() - start_time):
            send_time = time.time()
            packet = create_packet(identifier, seq, size)
            s.sendto(packet, (dest_ip, 1))
            sent += 1

            try:
                response, addr = s.recvfrom(1024)
                recv_time = time.time()
                rtt = (recv_time - send_time) * 1000  # Convert to ms
                rtt_list.append(rtt)
                received += 1

                # Extract TTL from IP header (byte 8)
                ttl = struct.unpack("!B", response[8:9])[0]

                print(f"{size} bytes from {addr[0]}: icmp_seq={seq} ttl={ttl} time={rtt:.1f} ms")

            except socket.timeout:
                print(f"Request timeout for icmp_seq {seq}")

            if count is None:
                time.sleep(interval)

            elif seq < count:
                time.sleep(interval)

            seq += 1   
    except KeyboardInterrupt:
        pass

    # Gathers all information for output's summary
    loss = ((sent - received) / sent) * 100
    total_time = int((time.time() - start_time) * 1000)

    print(f"\n--- {hostname or dest_ip} ping statistics ---")
    print(f"{sent} packets transmitted, {received} received, {loss:.0f}% packet loss, time {total_time}ms")

    if rtt_list:
        print(f"rtt min/avg/max/stddev = {min(rtt_list):.3f}/{sum(rtt_list)/len(rtt_list):.3f}/{max(rtt_list):.3f}/{(statistics.stdev(rtt_list)):.3f} ms")

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

def main():
    """Parse command-line arguments and initiate the ping process.
    
    This function handles user input, resolves the target hostname to an IP address,
    and calls the `send_ping` function to perform the ICMP Echo Request. The user can 
    specify the number of packets to send, the interval between packets, the payload size,
    and the timeout for the ping request.

    Command-line arguments:
        - host: Target IP address or hostname to ping.
        - -c: Number of packets to send.
        - -i: Interval (in seconds) between packets (default is 1.0).
        - -s: Payload size in bytes (default is 56).
        - -t: Timeout in seconds for the ping request.

    :return: None
    """
    parser = argparse.ArgumentParser(description="Unix-style Ping command")
    parser.add_argument("host", type=str, help="Target IP or Hostname")
    parser.add_argument("-c", type=int, default=None, help="Number of packets")
    parser.add_argument("-i", type=float, default=1.0, help="Interval between packets")
    parser.add_argument("-s", type=int, default=56, help="Payload size (default: 56 bytes)")
    parser.add_argument("-t", type=int, default=None, help="Timeout in seconds")

    args = parser.parse_args()
    
    ip, hostname = resolve_target(args.host)
    if ip:
        send_ping(ip, args.c, args.i, args.s, args.t, hostname)

if __name__ == '__main__':
    main()