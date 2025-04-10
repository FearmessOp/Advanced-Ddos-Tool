# DDoS Tool V2

![DDoS Tool Banner](https://cdn.glitch.global/20bb1161-dcd0-4cd9-af15-400cf2bf1f5c/20250411_0024_Fearmess%20Ddos%20Tan%C4%B1t%C4%B1m%C4%B1_simple_compose_01jrgs9vxae5p9fpc9abzhyh53%20(1).png?v=1744320400556)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Attack Types](#attack-types)
- [Command Line Parameters](#command-line-parameters)
- [Legal Disclaimer](#legal-disclaimer)
- [Creators](#creators)

## 🔍 Overview

DDoS Tool V2 is an educational tool developed for network security testing. This tool simulates various DDoS (Distributed Denial of Service) attack techniques to help system administrators test the resilience of their network infrastructure.

This tool is **ONLY** for educational purposes and should be used on your own systems or systems you have permission to test. Unauthorized use is illegal.

## ✨ Features

- **Advanced HTTP Attacks**: More effective attacks with random headers, paths, and parameters
- **SSL/TLS Support**: Ability to attack HTTPS sites
- **Slowloris Attack**: An effective method against web servers
- **Intensity Level**: Ability to adjust attack power on a scale of 1-10
- **Advanced Information Gathering**: Detailed analysis of the target
- **Multiple Attack Types**: TCP, UDP, HTTP, SYN, Slowloris, and HTTP-FLOOD
- **Real-time Statistics**: Detailed statistics during the attack
- **Command Line Support**: Run directly with command line parameters

## 💻 Installation

### Requirements

- Python 3.6 or higher
- The following Python libraries:
  - socket
  - threading
  - random
  - time
  - sys
  - os
  - re
  - ssl
  - json
  - argparse
  - datetime

### Installation Steps

1. Clone the repository or download the `ddos_tool_v2.py` file
2. Install the required libraries:

```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Using the Menu Interface

To start the program with the menu interface:

```bash
python ddos_tool_v2.py
```

This command starts an interactive menu interface and offers the following options:

1. **Start DDoS Attack**: Start an attack by specifying target IP/Domain, port, attack type, and other parameters
2. **Gather Information About Target**: Gather information about the target system (open ports, services, etc.)
3. **Help**: Show help information about the program
4. **Exit**: Exit the program

### Using the Command Line

To run the program directly with command line parameters:

```bash
python ddos_tool_v2.py -t <target> -p <port> -a <attack_type> -th <threads> -d <duration> -i <intensity>
```

Example:

```bash
python ddos_tool_v2.py -t example.com -p 80 -a http-flood -th 1000 -d 60 -i 5
```

## 💥 Attack Types

DDoS Tool V2 supports the following attack types:

### 1. TCP Flood

Creates TCP connections to keep the target system busy. Generally aims to exhaust the server's connection pool.

```bash
python ddos_tool_v2.py -t <target> -p <port> -a tcp
```

### 2. UDP Flood

Sends UDP packets to consume bandwidth. Aims to exhaust the target system's network resources.

```bash
python ddos_tool_v2.py -t <target> -p <port> -a udp
```

### 3. HTTP Flood

Sends HTTP requests to keep the web server busy. Targets web applications.

```bash
python ddos_tool_v2.py -t <target> -p 80 -a http
```

### 4. SYN Flood

Sends TCP SYN packets to exhaust the connection pool. Keeps the server busy by creating half-open connections.

```bash
python ddos_tool_v2.py -t <target> -p <port> -a syn
```

### 5. Slowloris

Creates slow and long-lasting HTTP connections to keep the web server busy. Can be effective with a small number of connections.

```bash
python ddos_tool_v2.py -t <target> -p 80 -a slowloris
```

### 6. HTTP-FLOOD (Advanced)

Sends intensive HTTP requests with random parameters and headers. More effective against web servers.

```bash
python ddos_tool_v2.py -t <target> -p 80 -a http-flood
```

## ⚙️ Command Line Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--target` | `-t` | Target IP or domain | - |
| `--port` | `-p` | Target port | - |
| `--attack` | `-a` | Attack type (tcp, udp, http, syn, slowloris, http-flood) | - |
| `--threads` | `-th` | Number of threads | 1000 |
| `--duration` | `-d` | Attack duration (seconds) | 60 |
| `--intensity` | `-i` | Intensity level (1-10) | 5 |
| `--ssl` | `-s` | Use SSL/TLS | False |
| `--path` | - | Path for HTTP request | / |

## ⚠️ Legal Disclaimer

This tool is **ONLY** for educational purposes and should be used on your own systems or systems you have permission to test. Unauthorized attacks on others' systems are illegal and can have serious legal consequences.

The user bears all responsibility for the use of this tool. The creators cannot be held responsible for misuse of the tool.

## 👨‍💻 Creators

- **Fearmess**
- Version: 2.0 - Advanced Version

---

## 📊 Performance Tips

- Use HTTP-FLOOD or Slowloris type for attacks on web servers
- Activate the SSL/TLS option and use port 443 for HTTPS sites
- Higher thread count and intensity level create more impact, but also strain your computer
- Press CTRL+C to stop the attack

## 🔒 Security Measures

To protect your systems against DDoS attacks:

1. Use a firewall and close unnecessary ports
2. Use DDoS protection services (Cloudflare, AWS Shield, etc.)
3. Set up traffic limiting and filtering mechanisms
4. Regularly monitor your server resources
5. Use load balancers
6. Set up automatic scaling systems

---

**Note**: This tool was developed to raise awareness about network security and to test the resilience of systems. It is important to use it within ethical boundaries.
