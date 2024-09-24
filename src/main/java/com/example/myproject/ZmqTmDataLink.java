package org.yamcs.tctm;

import org.yamcs.TmPacket;
import org.yamcs.YConfiguration;
import org.zeromq.ZMQ;

public class ZmqTmDataLink extends AbstractTmDataLink {
    private ZMQ.Socket zmqSocket;
    private Exception previousException = null;
    private long lastReceiveTime = System.currentTimeMillis();
    private static final long TIMEOUT_PERIOD = 30000;  // 30 seconds timeout

    @Override
    public void init(String instance, String name, YConfiguration config) {
        super.init(instance, name, config);
        ZMQ.Context context = ZMQ.context(1);
        zmqSocket = context.socket(ZMQ.SUB);
        zmqSocket.connect("tcp://localhost:5555");//zmqSocket.connect("tcp://<ZMQ_SERVER_IP>:<ZMQ_PORT>"); 
        zmqSocket.subscribe(new byte[0]); // Subscribe to all messages
    }

    @Override
    public Link.Status connectionStatus() {
        // Case 1: If the ZMQ socket is not initialized
        if (zmqSocket == null) {
            return Link.Status.DISABLED;
        }

        // Try to check if the socket is still connected and functioning
        try {
            zmqSocket.setReceiveTimeOut(1000);  // Set a short timeout
            byte[] testRecv = zmqSocket.recv();

            // If we get data, or there's no error, assume the socket is OK
            if (testRecv != null || zmqSocket.errno() == 0) {
                return Link.Status.OK;
            } else {
                return Link.Status.UNAVAIL;  // The socket is unavailable
            }
        } catch (Exception e) {
            return Link.Status.FAILED;  // An exception occurred, indicating failure
        }
    }
    
    // Checks if a failure condition was met, like an exception during data processing
    private boolean isFailureConditionMet() {
        // Case 1: Exception occurred during data reception
        if (previousException != null) {
            return true;
        }

        // Case 2: Timeout occurred without receiving data
        if ((System.currentTimeMillis() - lastReceiveTime) > TIMEOUT_PERIOD) {
            return true;
        }

        return false;
    }

    // Method to track and process the ZMQ data, tracking failure
    private void receiveData() {
        try {
            byte[] zmqData = zmqSocket.recv();
            if (zmqData != null) {
                lastReceiveTime = System.currentTimeMillis();  // Reset receive time
                TmPacket packet = new TmPacket(System.currentTimeMillis(), zmqData);
                processPacket(packet);
            }
        } catch (Exception e) {
            previousException = e;  // Track the exception for failure condition
        }
    }
    
    // Checks if the ZMQ server is reachable
    private boolean isServerReachable() {
        try {
            // Set a short timeout to avoid blocking for too long
            zmqSocket.setReceiveTimeOut(1000);  // 1 second timeout
            byte[] testRecv = zmqSocket.recv();

            // If we get data, or no error, assume the server is reachable
            if (testRecv != null || zmqSocket.errno() == 0) {
                return true;
            } else {
                return false;
            }
        } catch (Exception e) {
            return false;  // Server unreachable or error occurred
        }
    }

    @Override
    protected void doStart() {
        new Thread(() -> {
            try {
                while (true) {
                    receiveData();  // Process the incoming ZMQ data
                }
            } catch (Exception e) {
                notifyFailed(e);  // Notify if the service fails
            }
        }).start();

        notifyStarted();  // Notify that the service has started
    }

    @Override
    protected void doStop() {
        try {
            zmqSocket.close();
            notifyStopped();  // Notify that the service has stopped
        } catch (Exception e) {
            notifyFailed(e);  // Notify if the service fails during stop
        }
    }
}
