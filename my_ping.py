import argparse
import sphinx
import socket
import struct
import time
import os
import select

def calculate_checksum(src_string):
    nbits = (len(src_string) // 2) * 2
    count = 0
    checksum = 0

    while count < nbits:
        temp = src_string[count + 1] * 256 + src_string[count]
        checksum += temp
        checksum &= 0xffffffff
        count += 2
    
    if nbits < len(src_string):
        checksum += src_string[len(src_string) - 1]
        checksum &= 0xffffffff

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += (checksum >> 16)
    result = ~checksum
    result &= 0xffff
    result = result >> 0 | (result << 8 & 0xffff)
    return result

def create_packet(identifier, seq, packetsize):
    header = struct.pack('!BBHHH', 8, 0, 0, identifier, seq)
    payload = bytes(range(packetsize))
    checksum = calculate_checksum(header + payload)
    header = struct.pack('!BBHHH', 8, 0, checksum, identifier, seq)
    return header + payload

def send(dst, count, wait, packetsize, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.settimeout(timeout)

    identifier = int(time.time()) & 0xFFFF
    start_time = time.time()

    for seq in range(count):
        if time.time() - start_time >= timeout:
            break

        packet = create_packet(identifier, seq, packetsize)
        s.sendto(packet, (dst, 1)) 

        print(f"Sent ICMP Echo Request to {dst}, sequence = {seq}, size={packetsize}")

        try:
            s.recvfrom(1024)
            print(f"Received reply from {dst}")
        except s.timeout:
            print("Request timed out")
        
        if seq < count - 1:
            time.sleep(wait)


def main():
    pingParser = argparse.ArgumentParser(prog='my_ping', description='TODO')

    pingParser.add_argument("host", type=str, help="Target IP or Hostname")

    pingParser.add_argument("-c", type=int, default=float("inf"), 
                        help="Stop after sending (and receiving) count ECHO_RESPONSE packets. If not specified, runs until interrupted.")

    pingParser.add_argument("-i", type=float, default=1.0, 
                        help="Wait for wait seconds between sending each packet. Default is one second.")

    pingParser.add_argument("-s", type=int, default=56, 
                        help="Specify the number of data bytes to be sent. Default is 56 (64 ICMP data bytes including the header).")

    pingParser.add_argument("-t", type=int, default=10, 
                        help="Specify a timeout in seconds before ping exits regardless of how many packets have been received.")

    args = pingParser.parse_args()
    print(args)
    
    send(args.host, args.c, args.i, args.s, args.t)

if __name__ == '__main__':
    main()
