// package com.example.myproject.algorithms;
// import org.yamcs.parameter.ParameterValue;
// import org.yamcs.xtce.CustomAlgorithm;
// import org.yamcs.utils.ValueUtility;

// import java.util.List;
// import java.util.ArrayList;

// public class CustomTelemetryProcessingAlgorithm {

//     // Constructor, if needed for any initial setup
//     public CustomTelemetryProcessingAlgorithm() {
//         // No specific arguments, just a default constructor
//     }

//     // Method to run the algorithm and process the telemetry data
//     public void runAlgorithm(long acqTime, long genTime, List<ParameterValue> inputValues, List<ParameterValue> outputValues) {
//         // Process EPS data for each channel (assuming two channels as an example)
//         processEps(1, inputValues, outputValues);
//         processEps(2, inputValues, outputValues);
//     }

//     // Extract telemetry data by filtering parameter names (e.g., "TMP", "VOPT", "IOPT")
//     private List<ParameterValue> extractFromDatum(List<ParameterValue> input, String arg) {
//         List<ParameterValue> result = new ArrayList<>();
//         for (ParameterValue pv : input) {
//             if (pv.getParameter().getQualifiedName().contains(arg)) {
//                 result.add(pv);
//             }
//         }
//         return result;
//     }

//     // Process EPS telemetry data for a given channel (ch)
//     private void processEps(int ch, List<ParameterValue> input, List<ParameterValue> output) {
//         // Extract telemetry values: TMP (temperature), VOPT (voltage), IOPT (current)
//         List<ParameterValue> tmp = extractFromDatum(input, "TMP" + ch);
//         List<ParameterValue> vopt = extractFromDatum(input, "VOPT" + ch);
//         List<ParameterValue> iopt = extractFromDatum(input, "IOPT" + ch);

//         for (int i = 0; i < tmp.size(); i++) {
//             // Get raw values
//             double tmpValue = tmp.get(i).getEngValue().getFloatValue();
//             double voptValue = vopt.get(i).getEngValue().getFloatValue();
//             double ioptValue = iopt.get(i).getEngValue().getFloatValue();

//             // Perform conversion for EPS telemetry
//             EpsData epsData = convertEpsEq(tmpValue, voptValue, ioptValue, ch);

//             // Add converted values to output list
//             output.add(createParameterValue(tmp.get(i).getParameter().getQualifiedName() + "_voltage", epsData.voltage));
//             output.add(createParameterValue(tmp.get(i).getParameter().getQualifiedName() + "_current", epsData.current));
//             output.add(createParameterValue(tmp.get(i).getParameter().getQualifiedName() + "_temperature", epsData.temperature));
//         }
//     }

//     // Conversion logic for EPS data (voltage, current, temperature)
//     private EpsData convertEpsEq(double tmp, double vopt, double iopt, int ch) {
//         double voltage = 0;
//         double current = 0;
//         double temperature = 0;

//         if (ch == 1) {
//             voltage = (0.521 * vopt / 256 * 5) + 8.533;
//             current = (iopt * 5 / 256 - 1.6025) * 15;
//             temperature = (1 / (1 / 298.15 - Math.log(10000 / (5 - 5 / 256 * tmp)) / 4190)) - 273.15;
//         } else if (ch == 2) {
//             voltage = (1.034 * vopt / 256 * 5) + 18.286;
//             current = (iopt * 5 / 256 - 1.6182) * 15;
//             temperature = (1 / (1 / 298.15 - Math.log(10000 / (5 - 5 / 256 * tmp)) / 4190)) - 273.15;
//         }

//         return new EpsData(round(voltage, 2), round(current, 2), round(temperature, 2));
//     }

//     // Utility method to create a parameter value
//     private ParameterValue createParameterValue(String name, double value) {
//         ParameterValue pv = new ParameterValue(name);
//         pv.setEngineeringValue(ValueUtility.getFloatValue((float) value));  // Ensure it uses float for engineering value
//         return pv;
//     }

//     // Round the value to 2 decimal places
//     private double round(double value, int places) {
//         long factor = (long) Math.pow(10, places);
//         value = value * factor;
//         long tmp = Math.round(value);
//         return (double) tmp / factor;
//     }

//     // Helper class to store converted EPS data
//     private static class EpsData {
//         double voltage;
//         double current;
//         double temperature;

//         EpsData(double voltage, double current, double temperature) {
//             this.voltage = voltage;
//             this.current = current;
//             this.temperature = temperature;
//         }
//     }
// }
package com.example.myproject.algorithms;

import org.yamcs.parameter.ParameterValue;
import org.yamcs.utils.ValueUtility;

import java.util.List;
import java.util.ArrayList;

public class CustomTelemetryProcessingAlgorithm {

    // Constructor, if needed for any initial setup
    public CustomTelemetryProcessingAlgorithm() {
        // No specific arguments, just a default constructor
    }

    // Method to run the algorithm and process the telemetry data
    public void runAlgorithm(long acqTime, long genTime, List<ParameterValue> inputValues, List<ParameterValue> outputValues) {
        // Process EPS data for each channel (assuming two channels as an example)
        processEps(1, inputValues, outputValues);
        processEps(2, inputValues, outputValues);
    }

    // Extract telemetry data by filtering parameter names (e.g., "TMP", "VOPT", "IOPT")
    private List<ParameterValue> extractFromDatum(List<ParameterValue> input, String arg) {
        List<ParameterValue> result = new ArrayList<>();
        for (ParameterValue pv : input) {
            if (pv.getParameter().getQualifiedName().contains(arg)) {
                result.add(pv);
            }
        }
        return result;
    }

    // Process EPS telemetry data for a given channel (ch)
    private void processEps(int ch, List<ParameterValue> input, List<ParameterValue> output) {
        // Extract telemetry values: TMP (temperature), VOPT (voltage), IOPT (current)
        List<ParameterValue> tmp = extractFromDatum(input, "TMP" + ch);
        List<ParameterValue> vopt = extractFromDatum(input, "VOPT" + ch);
        List<ParameterValue> iopt = extractFromDatum(input, "IOPT" + ch);

        for (int i = 0; i < tmp.size(); i++) {
            // Get raw values
            double tmpValue = tmp.get(i).getEngValue().getFloatValue();
            double voptValue = vopt.get(i).getEngValue().getFloatValue();
            double ioptValue = iopt.get(i).getEngValue().getFloatValue();

            // Perform conversion for EPS telemetry
            EpsData epsData = convertEpsEq(tmpValue, voptValue, ioptValue, ch);

            // Add converted values to output list
            output.add(createParameterValue(tmp.get(i).getParameter().getQualifiedName() + "_voltage", epsData.voltage));
            output.add(createParameterValue(tmp.get(i).getParameter().getQualifiedName() + "_current", epsData.current));
            output.add(createParameterValue(tmp.get(i).getParameter().getQualifiedName() + "_temperature", epsData.temperature));
        }
    }

    // Conversion logic for EPS data (voltage, current, temperature)
    private EpsData convertEpsEq(double tmp, double vopt, double iopt, int ch) {
        double voltage = 0;
        double current = 0;
        double temperature = 0;

        if (ch == 1) {
            voltage = (0.521 * vopt / 256 * 5) + 8.533;
            current = (iopt * 5 / 256 - 1.6025) * 15;
            temperature = (1 / (1 / 298.15 - Math.log(10000 / (5 - 5 / 256 * tmp)) / 4190)) - 273.15;
        } else if (ch == 2) {
            voltage = (1.034 * vopt / 256 * 5) + 18.286;
            current = (iopt * 5 / 256 - 1.6182) * 15;
            temperature = (1 / (1 / 298.15 - Math.log(10000 / (5 - 5 / 256 * tmp)) / 4190)) - 273.15;
        }

        return new EpsData(round(voltage, 2), round(current, 2), round(temperature, 2));
    }

    // Utility method to create a parameter value
    private ParameterValue createParameterValue(String name, double value) {
        ParameterValue pv = new ParameterValue(name);
        pv.setEngineeringValue(ValueUtility.getFloatValue((float) value));  // Ensure it uses float for engineering value
        return pv;
    }

    // Round the value to 2 decimal places
    private double round(double value, int places) {
        long factor = (long) Math.pow(10, places);
        value = value * factor;
        long tmp = Math.round(value);
        return (double) tmp / factor;
    }

    // Helper class to store converted EPS data
    private static class EpsData {
        double voltage;
        double current;
        double temperature;

        EpsData(double voltage, double current, double temperature) {
            this.voltage = voltage;
            this.current = current;
            this.temperature = temperature;
        }
    }
}
