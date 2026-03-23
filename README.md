Here is a **complete professional `README.md`** for your project (no emojis, clean and ready for GitHub submission):

---

# Distributed Load Balancer with Health Monitoring and Dashboard (Python)

## Overview

This project implements a distributed load balancer using Python socket programming. It efficiently distributes incoming client requests across multiple backend servers using configurable load balancing algorithms. The system includes real-time health monitoring, fault tolerance mechanisms, and a web-based dashboard for visualization.

The project demonstrates key concepts in networking, distributed systems, and system design, making it suitable for academic and placement purposes.

---

## Features

* Multi-client handling using multithreading
* Load balancing algorithms:

  * Round Robin
  * Least Connections
  * Weighted Round Robin
* Real-time health monitoring of backend servers
* Fault tolerance with retry mechanism
* Dynamic server configuration using JSON
* Logging system for debugging and monitoring
* Metrics tracking (requests, connections, response time)
* Web-based dashboard using Flask
* Unit and integration testing

---

## System Architecture

Client requests are received by the load balancer, which selects an appropriate backend server using a chosen algorithm. The request is forwarded to the backend server, and the response is returned to the client. A health checker continuously monitors server availability, while a dashboard displays real-time system metrics.

---

## Project Structure

```
load_balancer_project/
│
├── backend/               # Backend servers (normal, slow, unstable)
├── core/                  # Core load balancer logic
├── config/                # Configuration files
├── dashboard/             # Web dashboard (Flask)
├── utils/                 # Helper utilities, constants, metrics
├── tests/                 # Unit and integration tests
├── logs/                  # Log files
│
├── main.py                # Entry point
├── requirements.txt       # Dependencies
└── README.md
```

---

## Technologies Used

* Python 3
* Socket Programming
* Multithreading
* Flask (for dashboard)
* JSON (configuration)
* Logging module

---

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/load-balancer-project.git
cd load-balancer-project
```

2. Install dependencies:

```
pip install -r requirements.txt
```

---

## Configuration

Backend servers are defined in:

```
config/servers.json
```

Example:

```
{
  "servers": [
    {"id": "S1", "host": "127.0.0.1", "port": 9001},
    {"id": "S2", "host": "127.0.0.1", "port": 9002}
  ]
}
```

Load balancing algorithm can be set in:

```
config/settings.py
```

```
ALGORITHM = "round_robin"
```

Options:

* round_robin
* least_connections
* weighted

---

## How to Run

### Step 1: Start Backend Servers

Open multiple terminals and run:

```
python backend/server.py --port 9001 --id S1
python backend/server.py --port 9002 --id S2
python backend/slow_server.py --port 9003 --id SLOW
python backend/unstable_server.py --port 9004 --id UNSTABLE
```

---

### Step 2: Start the System

```
python main.py
```

---

### Step 3: Access the Application

Load Balancer:

```
http://127.0.0.1:8080
```

Dashboard:

```
http://127.0.0.1:5000
```

---

## Testing

Run unit and integration tests:

```
python tests/test_algorithms.py
python tests/test_balancer.py
python tests/test_health.py
```

---

## Logging

Logs are stored in:

```
logs/app.log
```

They include:

* Request handling
* Server status
* Errors and failures

---

## Key Concepts Demonstrated

* Socket programming and TCP communication
* Concurrent client handling using threads
* Load balancing strategies
* Fault tolerance and retry mechanisms
* Health monitoring in distributed systems
* Modular software design
* Real-time system visualization

---

## Use Cases

* Understanding distributed systems
* Learning network programming
* Academic projects
* Interview preparation
* System design demonstrations

---

## Future Enhancements

* HTTPS support
* Dynamic scaling of backend servers
* WebSocket-based real-time updates
* Machine learning-based load prediction
* Containerization using Docker

---

## Author

Varshini G S
Amrita Vishwa Vidyapeetham, Coimbatore

---

## License

This project is for educational purposes.
