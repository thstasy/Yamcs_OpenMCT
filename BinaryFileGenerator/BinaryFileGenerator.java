import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.time.Instant;

public class BinaryFileGenerator {

    // Ports for telemetry and telecommands
    private static final int[] TELEMETRY_PORTS = {5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008, 5009}; // Telemetry ports
    private static final int COMMAND_PORT = 10025;  // Telecommand port

    public static void main(String[] args) {
        try {
            // Generate binary files for each telemetry port
            for (int port : TELEMETRY_PORTS) {
                generateTelemetryBinaryFile(port);
            }

            // Generate binary file for telecommands
            generateTelecommandBinaryFile(COMMAND_PORT);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Method to generate binary files for telemetry data
    private static void generateTelemetryBinaryFile(int port) throws IOException {
        // Create the binary data for telemetry
        ByteBuffer buffer = ByteBuffer.allocate(24).order(ByteOrder.BIG_ENDIAN);  // 24 bytes for example

        int sequenceCount = 1;  // Example sequence count
        long timestamp = Instant.now().toEpochMilli();  // Current timestamp in milliseconds
        byte[] payload = new byte[]{0x01, 0x02, 0x03, 0x04};  // Example payload

        // Pack the data into the buffer
        buffer.putInt(sequenceCount);           // 4 bytes: sequence count
        buffer.putLong(timestamp);              // 8 bytes: timestamp
        buffer.put(payload);                    // 4 bytes: payload
        buffer.putInt(0x0000);                  // Example placeholder data
        buffer.putInt(port);                    // 4 bytes: port-specific data (unique to this telemetry)

        // Write the buffer to a file
        try (FileOutputStream fos = new FileOutputStream("udp_payload_" + port + ".bin")) {
            fos.write(buffer.array());
            System.out.println("Generated telemetry file for port " + port);
        }
    }

    // Method to generate binary file for telecommand data
    private static void generateTelecommandBinaryFile(int port) throws IOException {
        // Create the binary data for telecommands
        ByteBuffer buffer = ByteBuffer.allocate(16).order(ByteOrder.BIG_ENDIAN);  // 16 bytes for example

        int commandId = 0x01020304;            // Example telecommand ID
        byte[] commandParams = new byte[]{0x05, 0x06, 0x07, 0x08};  // Command parameters

        // Pack the data into the buffer
        buffer.putInt(commandId);              // 4 bytes: command ID
        buffer.put(commandParams);             // 4 bytes: command parameters
        buffer.putLong(Instant.now().toEpochMilli());  // 8 bytes: timestamp

        // Write the buffer to a file
        try (FileOutputStream fos = new FileOutputStream("udp_payload_" + port + ".bin")) {
            fos.write(buffer.array());
            System.out.println("Generated telecommand file for port " + port);
        }
    }
}
