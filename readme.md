
# my_ping.py

This Python script mimics the behavior of the `ping` command, sending ICMP Echo Request packets to a specified target (IP address or hostname). It provides useful statistics like round-trip time (RTT) and packet loss. 

## Requirements

- Python 3.x
- `socket` and `struct` libraries (These are part of the Python standard library, so no additional installation is required.)

## How to Compile and Run the Code

This script does not require compilation since it's written in Python. To run the script, use the following command in your terminal:

```bash
python3 ping_tool.py [OPTIONS] TARGET
```

### Options:
- `-c count` : Number of packets to send.
- `-i wait` : Time interval (in seconds) between each packet (default is 1 second).
- `-s packetsize` : Size of the ICMP payload in bytes (default is 56 bytes).
- `-t timeout` : Timeout in seconds for waiting for a reply.

### Example Command-Line Usage

1. **Basic Ping to a Host**  
   This command sends 4 ping requests to `example.com` with the default interval and packet size.
   
   ```bash
   python3 ping_tool.py example.com -c 4
   ```

2. **Ping with Custom Interval and Packet Size**  
   This command sends 10 ping requests to `192.168.1.1`, with a 0.5-second interval between packets and a payload size of 128 bytes.
   
   ```bash
   python3 ping_tool.py 192.168.1.1 -c 10 -i 0.5 -s 128
   ```

3. **Ping with Timeout**  
   This command sends 5 ping requests to `example.com`, with a timeout of 2 seconds per request.
   
   ```bash
   python3 ping_tool.py example.com -c 5 -t 2
   ```

4. **Unlimited Ping**  
   This command pings `google.com` indefinitely with the default settings until interrupted by the user (Ctrl + C).
   
   ```bash
   python3 ping_tool.py google.com
   ```

## Output

The script will output the following information for each ping request:
- The size of the ICMP packet sent
- The IP address of the target host
- The round-trip time (RTT) in milliseconds
- The TTL (Time to Live) value from the IP header

At the end, you'll see a summary of the ping statistics, including:
- Total packets transmitted
- Total packets received
- Packet loss percentage
- Minimum, average, maximum, and standard deviation of RTT values

## Example Output

```plaintext
PING example.com (93.184.216.34) 56 bytes of data.
64 bytes from 93.184.216.34: icmp_seq=1 ttl=56 time=15.5 ms
64 bytes from 93.184.216.34: icmp_seq=2 ttl=56 time=14.8 ms
64 bytes from 93.184.216.34: icmp_seq=3 ttl=56 time=15.2 ms
64 bytes from 93.184.216.34: icmp_seq=4 ttl=56 time=14.9 ms

--- example.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 14.802/15.125/15.522/0.271 ms
```

## Notes
- The script needs to be run with root/administrator privileges to use raw sockets for sending ICMP packets.
- The target host can be specified by IP address or hostname.
- If the target is a domain name, it will be resolved to an IP address automatically.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
