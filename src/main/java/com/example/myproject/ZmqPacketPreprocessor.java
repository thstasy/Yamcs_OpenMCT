// package com.example.myproject;

// import java.nio.ByteBuffer;
// import org.yamcs.TmPacket;
// import org.yamcs.YConfiguration;
// import org.yamcs.tctm.AbstractPacketPreprocessor;
// import org.yamcs.utils.TimeEncoding;

/**
 * Custom Packet Preprocessor for ZMQ telemetry data.
 */
/*
public class ZmqPacketPreprocessor extends AbstractPacketPreprocessor {

    // Constructor used when this preprocessor is used without YAML configuration
    public ZmqPacketPreprocessor(String yamcsInstance) {
        this(yamcsInstance, YConfiguration.emptyConfig());
    }

    // Constructor used when this preprocessor is used with YAML configuration
    public ZmqPacketPreprocessor(String yamcsInstance, YConfiguration config) {
        super(yamcsInstance, config);
    }

    @Override
    public TmPacket process(TmPacket packet) {
        byte[] bytes = packet.getPacket();

        // Add custom logic for processing ZMQ packets here
        if (bytes.length < 10) {  // Adjust based on your ZMQ data format
            eventProducer.sendWarning("SHORT_PACKET", "Short ZMQ packet received, length: " + bytes.length);
            return null;  // Drop the packet if it's too short
        }

        // Process ZMQ packet (adjust this based on your actual data format)
        ByteBuffer buffer = ByteBuffer.wrap(bytes);
        int customField = buffer.getInt(0);  // Example: extract a field from the ZMQ packet

        // Set the packet's generation time (current wallclock time)
        packet.setGenerationTime(TimeEncoding.getWallclockTime());

        // Set a custom sequence count or identifier
        packet.setSequenceCount(customField);  // Example: Use customField as sequence count

        return packet;
    }
}
*/

package com.example.myproject;

import java.nio.ByteBuffer;
import org.yamcs.TmPacket;
import org.yamcs.YConfiguration;
import org.yamcs.tctm.AbstractPacketPreprocessor;
import org.yamcs.utils.TimeEncoding;

/**
 * Custom Packet Preprocessor for ZMQ telemetry data.
 */
public class ZmqPacketPreprocessor extends AbstractPacketPreprocessor {

    // Constructor used when this preprocessor is used without YAML configuration
    public ZmqPacketPreprocessor(String yamcsInstance) {
        this(yamcsInstance, YConfiguration.emptyConfig());
    }

    // Constructor used when this preprocessor is used with YAML configuration
    public ZmqPacketPreprocessor(String yamcsInstance, YConfiguration config) {
        super(yamcsInstance, config);
    }

    @Override
    public TmPacket process(TmPacket packet) {
        byte[] bytes = packet.getPacket();

        // Add custom logic for processing ZMQ packets here
        if (bytes.length < 10) {
            eventProducer.sendWarning("SHORT_PACKET", "Short ZMQ packet received, length: " + bytes.length);
            return null;
        }

        // Process ZMQ packet based on telemetry binary data format
        ByteBuffer buffer = ByteBuffer.wrap(bytes);

        // Example of extracting telemetry fields
        int timestamp = buffer.getInt(0);  // Extract timestamp
        int sequenceCount = buffer.getInt(4);  // Extract sequence count
        int sensorValue1 = buffer.getShort(8);  // Extract sensor value 1
        int sensorValue2 = buffer.getShort(10);  // Extract sensor value 2

        // Set packet metadata
        packet.setGenerationTime(TimeEncoding.getWallclockTime());
        packet.setSequenceCount(sequenceCount);  // Use the extracted sequence count

        // Further processing (e.g., storing sensor values, etc.) could be added here

        return packet;
    }
}
