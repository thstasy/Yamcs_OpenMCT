import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.time.Instant;

public class UdpTelemetrySimulator {

    // Define UDP Ports for different telemetry links
    private static final int UDP_PORT_FSW = 5001;
    private static final int UDP_PORT_DAQ_AVI = 5002;
    private static final int UDP_PORT_DAQ_ACC = 5003;
    private static final int UDP_PORT_GPSR = 5004;
    private static final int UDP_PORT_RTK = 5005;
    private static final int UDP_PORT_IMU_PAYLOAD = 5006;
    private static final int UDP_PORT_IPCAM1 = 5007;
    private static final int UDP_PORT_IPCAM2 = 5008;
    private static final int UDP_PORT_IPCAM3 = 5009;
    private static final String UDP_IP = "127.0.0.1";  // Change if needed

    private static int sequenceCount = 0;  // Initialize sequence count
    private static final Object lock = new Object();  // Lock object for synchronization

    public static void main(String[] args) {
        try (DatagramSocket socket = new DatagramSocket()) {  // Using try-with-resources for clean socket closure

            // Simulate data and send for each link
            while (true) {
                // Send telemetry data for all UDP ports
                sendTelemetryData(socket, UDP_PORT_FSW, generateFsTelemetry());
                sendTelemetryData(socket, UDP_PORT_DAQ_AVI, generateDaqAviTelemetry());
                sendTelemetryData(socket, UDP_PORT_DAQ_ACC, generateDaqAccTelemetry());
                sendTelemetryData(socket, UDP_PORT_GPSR, generateGpsrTelemetry());
                sendTelemetryData(socket, UDP_PORT_RTK, generateRtkTelemetry());
                sendTelemetryData(socket, UDP_PORT_IMU_PAYLOAD, generateImuTelemetry());
                sendTelemetryData(socket, UDP_PORT_IPCAM1, generateIpcamTelemetry(1));
                sendTelemetryData(socket, UDP_PORT_IPCAM2, generateIpcamTelemetry(2));
                sendTelemetryData(socket, UDP_PORT_IPCAM3, generateIpcamTelemetry(3));

                // Sleep for a second before sending the next batch of telemetry data
                Thread.sleep(1000);  // Adjust as needed for real-time simulation
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Method to send data through UDP
    private static void sendTelemetryData(DatagramSocket socket, int port, byte[] data) throws Exception {
        InetAddress address = InetAddress.getByName(UDP_IP);
        DatagramPacket packet = new DatagramPacket(data, data.length, address, port);

        // Log packet size and port number
        System.out.println("Telemetry sent to port " + port + " | Packet size: " + data.length + " bytes");

        socket.send(packet);
    }


    private static byte[] generateTelemetryData(byte[] payload) {
        ByteBuffer buffer = ByteBuffer.allocate(20 + payload.length).order(ByteOrder.BIG_ENDIAN);  // Ensure Big Endian order
    
        // Synchronized block to prevent ConcurrentModificationException
        synchronized (lock) {
            // Add 4-byte sequence count at offset 0 (Yamcs expects sequence count at offset 4)
            buffer.putInt(sequenceCount);
            sequenceCount++;  // Increment sequence count for the next packet
        }
    
        // Use a fixed timestamp for testing purposes (e.g., 1625097600 is equivalent to 2021-07-01T00:00:00Z)
        long fixedTimestamp = 1625097600000L;  // Fixed timestamp in milliseconds (2021-07-01)
        System.out.println("Generated Fixed Timestamp (milliseconds): " + fixedTimestamp);  // Log the fixed timestamp
        buffer.putLong(fixedTimestamp);
    
        // Add the rest of the telemetry payload
        buffer.put(payload);
    
        return buffer.array();  // Return the full packet with the required structure
    }

    // Generate sample data for FSW (Flight Software)
    private static byte[] generateFsTelemetry() {
        byte[] payload = new byte[]{0x01, 0x02, 0x03, 0x04};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }

    // Generate sample data for DAQ-AVI (Data Acquisition - AVI)
    private static byte[] generateDaqAviTelemetry() {
        byte[] payload = new byte[]{0x05, 0x06, 0x07, 0x08};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }

    // Generate sample data for DAQ-ACC (Data Acquisition - Accelerometer)
    private static byte[] generateDaqAccTelemetry() {
        byte[] payload = new byte[]{0x09, 0x0A, 0x0B, 0x0C};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }

    // Generate sample data for GPSR (GPS Receiver)
    private static byte[] generateGpsrTelemetry() {
        byte[] payload = new byte[]{0x0D, 0x0E, 0x0F, 0x10};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }

    // Generate sample data for RTK (Real-Time Kinematic)
    private static byte[] generateRtkTelemetry() {
        byte[] payload = new byte[]{0x11, 0x12, 0x13, 0x14};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }

    // Generate sample data for IMU Payload (Inertial Measurement Unit)
    private static byte[] generateImuTelemetry() {
        byte[] payload = new byte[]{0x15, 0x16, 0x17, 0x18};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }

    // Generate sample data for IPCAM (IP Camera) - for each camera
    private static byte[] generateIpcamTelemetry(int camNumber) {
        byte[] payload = new byte[]{(byte) camNumber, 0x19, 0x1A, 0x1B};  // Example payload data (4 bytes)
        return generateTelemetryData(payload);  // Add sequence count and timestamp
    }
}
