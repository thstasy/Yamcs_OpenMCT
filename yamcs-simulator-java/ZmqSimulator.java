import org.zeromq.ZMQ;

public class ZmqSimulator {
    public static void main(String[] args) {
        ZMQ.Context context = ZMQ.context(1);
        ZMQ.Socket socket = context.socket(ZMQ.PUB);  // PUB socket to send data

        socket.bind("udp://localhost:5555");  // Bind to UDP port 5555

        int count = 0;
        while (!Thread.currentThread().isInterrupted()) {
            String message = "Telemetry data " + count;
            System.out.println("Sending: " + message);
            socket.send(message.getBytes(), 0);  // Send the data
            count++;
            try {
                Thread.sleep(1000);  // Send every second
            } catch (InterruptedException e) {
                break;
            }
        }
        socket.close();
        context.term();
    }
}
