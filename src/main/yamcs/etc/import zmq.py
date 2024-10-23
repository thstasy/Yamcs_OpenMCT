import zmq

# Set up the ZMQ context and DISH socket for receiving UDP data
context = zmq.Context()
zmq_socket = context.socket(zmq.DISH)
zmq_socket.bind("udp://*:5555")  # Bind to the same port as Yamcs ZMQ UDP data link

# Subscribe to any group (wildcard)
zmq_socket.join("")

print("Waiting for telemetry data...")

while True:
    message = zmq_socket.recv()
    print(f"Received message: {message}")
