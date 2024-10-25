import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class UdpSimulators {

    // UDP Ports for telemetry and telecommands
    private static final int TELEMETRY_PORT = 5001;   // Telemetry data port
    private static final int COMMAND_PORT = 10025;    // Telecommand port
    private static final String UDP_IP = "127.0.0.1"; // IP address

    // Main method to run the simulators
    public static void main(String[] args) {
        try {
            DatagramSocket socket = new DatagramSocket();

            // Simulate sending telemetry and telecommands in a loop
            while (true) {
                // Send telemetry data
                sendTelemetry(socket, TELEMETRY_PORT, generateTelemetryData());

                // Simulate sending a telecommand
                sendTelecommand(socket, COMMAND_PORT, generateTelecommandData());

                // Pause for a second between sending data
                Thread.sleep(1000);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Method to send telemetry data
    private static void sendTelemetry(DatagramSocket socket, int port, byte[] telemetryData) throws Exception {
        InetAddress address = InetAddress.getByName(UDP_IP);
        DatagramPacket packet = new DatagramPacket(telemetryData, telemetryData.length, address, port);

        // Log telemetry data
        System.out.println("Telemetry sent to port " + port + ": " + telemetryData.length + " bytes");

        socket.send(packet);
    }

    // Method to send telecommands
    private static void sendTelecommand(DatagramSocket socket, int port, byte[] commandData) throws Exception {
        InetAddress address = InetAddress.getByName(UDP_IP);
        DatagramPacket packet = new DatagramPacket(commandData, commandData.length, address, port);

        // Log telecommand data
        System.out.println("Telecommand sent to port " + port + ": " + commandData.length + " bytes");

        socket.send(packet);
    }

    // Generate telemetry data (simulated)
    private static byte[] generateTelemetryData() {
        ByteBuffer buffer = ByteBuffer.allocate(16).order(ByteOrder.BIG_ENDIAN);

        // Example telemetry: Sequence count and fixed timestamp
        buffer.putInt(0x0001); // Sequence count
        buffer.putLong(System.currentTimeMillis()); // Timestamp
        buffer.put(new byte[]{0x01, 0x02, 0x03, 0x04}); // Example payload

        return buffer.array();
    }

    // Generate telecommand data (simulated)
    private static byte[] generateTelecommandData() {
        ByteBuffer buffer = ByteBuffer.allocate(8).order(ByteOrder.BIG_ENDIAN);

        // Example telecommand: ID and command parameters
        buffer.putInt(0x01020304); // Command ID
        buffer.put(new byte[]{0x05, 0x06, 0x07, 0x08}); // Command parameters

        return buffer.array();
    }
}
