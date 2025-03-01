
## Requirements

- Python 3.x
- `socket` and `struct` libraries (These are part of the Python standard library, so no additional installation is required.)

# my_ping.py

This Python script mimics the behavior of the `ping` command, sending ICMP Echo Request packets to a specified target (IP address or hostname). It provides useful statistics like round-trip time (RTT) and packet loss. 

## How to Compile and Run the Code

This script does not require compilation since it's written in Python. To run the script, use the following command in your terminal:

```bash
python3 my_ping.py [OPTIONS] TARGET
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
   python3 my_ping.py example.com -c 4
   ```

2. **Ping with Custom Interval and Packet Size**  
   This command sends 10 ping requests to `192.168.1.1`, with a 0.5-second interval between packets and a payload size of 128 bytes.
   
   ```bash
   python3 my_ping.py 192.168.1.1 -c 10 -i 0.5 -s 128
   ```

3. **Ping with Timeout**  
   This command sends 5 ping requests to `example.com`, with a ending after of 2 seconds.
   
   ```bash
   python3 my_ping.py example.com -c 5 -t 2
   ```

4. **Unlimited Ping**  
   This command pings `google.com` indefinitely with the default settings until interrupted by the user (Ctrl + C).
   
   ```bash
   python3 my_ping.py google.com
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

# my_traceroute.py

This Python script mimics the behavior of the `traceroute` command, sending ICMP Echo Request packets to a specified target (IP address or hostname) with varying Time-To-Live (TTL) values. It shows the route packets take to reach the destination and provides useful statistics like round-trip time (RTT) and packet loss at each hop.

## How to Compile and Run the Code

This script also does not require compilation since it's written in Python. To run the script, use the following command in your terminal:

```bash
python3 my_traceroute.py [OPTIONS] TARGET
```

### Options:
- `-n` : Print hop addresses numerically rather than symbolically and numerically.
- `-q nqueries` : Set the number of probes per TTL to nqueries.
- `-S packetsize` : Print a summary of how many probes were not answered for each hop.

### Example Command-Line Usage

1. **Basic Traceroute to a Host**  
   This command performs a traceroute to example.com with the default number of hops (64) and probe count (3).
   
   ```bash
   python3 my_traceroute.py example.com
   ```

2. **Traceroute with Custom Probe Count**  
   This command performs a traceroute to 192.168.1.1 with 5 probes per TTL.
   
   ```bash
   python3 my_traceroute.py -q 5 192.168.1.1
   ```

3. **Traceroute with Numerical Addresses Only**  
   This command performs a traceroute to google.com, printing only IP addresses without resolving hostnames.
   
   ```bash
   python3 my_traceroute.py -n google.com
   ```

4. **Traceroute with Summary of Unanswered Probes**  
   This command performs a traceroute to example.com and prints a summary of packet loss per hop.
   
   ```bash
   python3 my_traceroute.py -S example.com
   ```

## Output

The script will output the following information for each hop:
- The TTL (Time-to-Live) value for the hop.
- The IP address (or hostname, if not using the `-n` option) of the intermediate device.
- The round-trip time (RTT) for each probe.

At the end, you'll see a list of the hops taken to get to the destination, including the loss per hop if `-S` is used

## Example Output

```plaintext
Traceroute to 8.8.8.8 (8.8.8.8), 64 hops max, 40 byte packets
 1 10.200.193.129 (10.200.193.129) 4.198 ms 4.943 ms 3.564 ms (0% loss) 
 2 10.5.153.1 (10.5.153.1) 15.679 ms 28.325 ms 17.597 ms (0% loss) 
 3 e0-8.core1.cle1.he.net (216.66.39.65) 17.783 ms 17.584 ms 16.978 ms (0% loss)
 4 100ge0-35.core2.det1.he.net (184.104.192.201) 21.339 ms 22.263 ms 21.745 
ms (0% loss)
 5 * * * (100% loss) 
 6 eqix-ch-100g.google.com (208.115.137.21) 31.292 ms 29.766 ms 30.563 ms (0% loss)
 7 142.251.249.49 (142.251.249.49) 28.686 ms 35.878 ms 30.056 ms (0% loss) 
 8 142.251.60.15 (142.251.60.15) 38.625 ms 29.536 ms 28.053 ms (0% loss) 
 9 dns.google (8.8.8.8) 28.167 ms 27.910 ms 27.007 ms (0% loss) 
```

## Notes
- Both scripts needs to be run with root/administrator privileges to use raw sockets for sending ICMP packets.
- The target host can be specified by IP address or hostname.
- If the target is a domain name, it will be resolved to an IP address automatically.