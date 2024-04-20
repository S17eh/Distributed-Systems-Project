# Distributed System with Pyro4

This project demonstrates the implementation of a distributed system using Python and the Pyro4 library. The system consists of two replicas that store key-value pairs and a client that interacts with these replicas.

## Prerequisites

- Python 3.x
- Pyro4

## Installation

1. Install Python from the official Python website.

2. Install Pyro4 using pip:

   ```
   pip install Pyro4

   ```

## Running the Project

### On the Server Machine:

1. Start the Pyro4 name server:

   ```
   pyro4-ns or python -m Pyro4.naming

   ```

   Keep this running in the background.

2. Run the server script:

   ```
   python server.py

   ```

### On the Client Machine:

1. (Only needed if serevr is on different machines, not needed if server is on local host and skip to step 2)

   All the machines should be on the same network, given that firewall of that network allows our request.
   (We faced that on some machines it was not allowed by the firewall. In that case you may want to just simulate on localhost.)

   Set the `PYRO_NS_HOSTNAME` environment variable to the IP address of the server machine:

   ```
   export PYRO_NS_HOSTNAME=server_ip
   (On windows use 'set' instead of 'export')

   ```

   Replace `server_ip` with the actual IP address of your server machine.

2. Run the client script:

   ```
   python client.py

   ```

## Project Structure

- `server.py`: This script creates two replicas and registers them with the Pyro4 name server. Each replica maintains its own data and a logical clock.

- `client.py`: This script interacts with the replicas by sending write, read, and delete requests.
