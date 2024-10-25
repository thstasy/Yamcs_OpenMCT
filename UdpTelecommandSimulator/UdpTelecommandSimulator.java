import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class UdpTelecommandSimulator {

    private static final String UDP_IP = "127.0.0.1";  // Target host (Yamcs server)
    private static final int UDP_PORT_OUT = 10025;     // UDP port for telecommands (from Yamcs config)
    
    private static int sequenceCount = 0;              // Sequence counter for telecommands
    private static final Object lock = new Object();   // Lock for synchronizing sequence count

    public static void main(String[] args) {
        try (DatagramSocket socket = new DatagramSocket()) {

            // Continuously send telecommands
            while (true) {
                // Send telecommand data
                sendTelecommandData(socket, UDP_PORT_OUT, generateTelecommandData());

                // Sleep for 1 second before sending the next telecommand
                Thread.sleep(1000);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Method to send telecommand data through UDP
    private static void sendTelecommandData(DatagramSocket socket, int port, byte[] data) throws Exception {
        InetAddress address = InetAddress.getByName(UDP_IP);
        DatagramPacket packet = new DatagramPacket(data, data.length, address, port);

        // Log packet size and port number
        System.out.println("Telecommand sent to port " + port + " | Packet size: " + data.length + " bytes");

        socket.send(packet);
    }

    // Generate a telecommand data packet with a sequence count and timestamp
    private static byte[] generateTelecommandData() {
        byte[] payload = new byte[]{0x01, 0x02, 0x03, 0x04};  // Example payload (replace with real telecommand)
        ByteBuffer buffer = ByteBuffer.allocate(20 + payload.length).order(ByteOrder.BIG_ENDIAN);  // 20 bytes for header + payload

        // Synchronized block to prevent sequence count conflicts
        synchronized (lock) {
            // Add 4-byte sequence count at offset 0
            buffer.putInt(sequenceCount);
            sequenceCount++;  // Increment sequence count for the next packet
        }

        // Use a fixed timestamp (replace this with real-time timestamp if necessary)
        long timestamp = System.currentTimeMillis();  // Get current timestamp in milliseconds
        System.out.println("Generated Timestamp (milliseconds): " + timestamp);
        buffer.putLong(timestamp);  // Add the 8-byte timestamp to the packet

        // Add the telecommand payload
        buffer.put(payload);

        return buffer.array();  // Return the constructed telecommand packet
    }
}
