import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class CreateBinaryTelecommand {

    private static final String BINARY_FILE_PATH = "udp_payload.bin";  // Binary file name

    public static void main(String[] args) {
        try {
            // Generate telecommand data
            byte[] commandPayload = generateTelecommandData();

            // Save the data to a binary file
            saveToFile(commandPayload, BINARY_FILE_PATH);
            System.out.println("Telecommand data written to " + BINARY_FILE_PATH);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Method to generate telecommand data
    private static byte[] generateTelecommandData() {
        ByteBuffer buffer = ByteBuffer.allocate(20).order(ByteOrder.BIG_ENDIAN);

        // Example telecommand data (you can modify this based on your requirements)
        buffer.putInt(123456);   // Command ID or sequence number
        buffer.putLong(System.currentTimeMillis());  // Timestamp for telecommand
        buffer.put(new byte[] {0x01, 0x02, 0x03, 0x04});  // Example command payload

        return buffer.array();
    }

    // Method to save binary data to a file
    private static void saveToFile(byte[] data, String filePath) throws IOException {
        try (FileOutputStream fos = new FileOutputStream(filePath)) {
            fos.write(data);
        }
    }
}
