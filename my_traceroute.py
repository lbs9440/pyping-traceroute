import argparse
import socket
import struct
import time
import os
import select
import statistics

def main():
    parser = argparse.ArgumentParser(description="Unix-style Ping")
    parser.add_argument("host", type=str, help="Target IP or Hostname for traceroute")
    parser.add_argument("-n", action='store_true', help='Print hop addresses numerially')
    parser.add_argument("-q", type=int, default=3, help="Number of probes per TTL (default: 3)")
    parser.add_argument("-S", action='store_true', help="Print summary of how many probes were not answered per hop")

    args = parser.parse_args()
    

if __name__ == '__main__':
    main()