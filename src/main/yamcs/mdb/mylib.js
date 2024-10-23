// function execute(telemetry) {
//     var processed = {};

//     // Process FSW Telemetry based on sid
//     if (telemetry.sid == 0x81B) {
//         processed.acceleration = processIMU(telemetry);
//     } else if (telemetry.sid == 0x838) {
//         processed.tvc = processTVC(telemetry);
//     } else if (telemetry.sid == 0x81E) {
//         processed.gpsr = processGPSR(telemetry);
//     } else if (telemetry.sid == 0x81F) {
//         processed.eps = processEPS(telemetry);
//     } else {
//         processed.rawData = telemetry;
//     }

//     return processed;
// }

// function processIMU(telemetry) {
//     return telemetry.imu('accel');
// }

// function processTVC(telemetry) {
//     var tvcData = [];
//     for (var i = 0; i < telemetry.tvc_tlm.tvc.length; i++) {
//         var tvcValues = telemetry.tvc_tlm.tvc[i].fvalues();
//         tvcData.push({
//             current_actual_value: tvcValues[1],
//             target_position: tvcValues[4],
//             pos_demand_value: tvcValues[6]
//         });
//     }
//     return tvcData;
// }

// function processGPSR(telemetry) {
//     var gpsr = telemetry.gpsr_data;
//     var lla = convertECEFToLLA(gpsr.ecef[0], gpsr.ecef[1], gpsr.ecef[2]);
//     return lla;
// }

// function processEPS(telemetry) {
//     var epsData = [];
//     var channels = [1, 2];
    
//     // Replace the for...of loop with a traditional for loop
//     for (var i = 0; i < channels.length; i++) {
//         var ch = channels[i];
//         var epsValues = getEPSValues(telemetry, ch);
//         epsData.push(epsValues);
//     }
    
//     return epsData;
// }


// function convertECEFToLLA(ecefX, ecefY, ecefZ) {
//     return [ecefX, ecefY, ecefZ];
// }

// function getEPSValues(telemetry, ch) {
//     var epsVoltage = telemetry.eps_tlm['VOPT' + ch];
//     var epsCurrent = telemetry.eps_tlm['IOPT' + ch];
//     var epsTemp = telemetry.eps_tlm['TMP' + ch];
//     return {
//         voltage: epsVoltage,
//         current: epsCurrent,
//         temperature: epsTemp
//     };
// }
function execute(telemetry) {
    var processed = {};

    // Process FSW Telemetry based on sid
    switch (telemetry.sid) {
        case 0x81B:
            processed.acceleration = processIMU(telemetry);
            break;
        case 0x838:
            processed.tvc = processTVC(telemetry);
            break;
        case 0x81E:
            processed.gpsr = processGPSR(telemetry);
            break;
        case 0x81F:
            processed.eps = processEPS(telemetry);  // Existing EPS processing
            break;
        case 0x820:  // Assuming 0x820 for Custom Algorithm SID (adjust as necessary)
            // Apply custom telemetry processing algorithm
            processed.customTelemetry = CustomTelemetryProcessingAlgorithm(
                telemetry.sunsensor, 
                telemetry.voltage, 
                telemetry.temperature
            );
            break;
        default:
            processed.rawData = telemetry;  // Store raw telemetry if the SID doesn't match predefined cases
            break;
    }

    return processed;
}

// Custom Telemetry Processing Algorithm
function CustomTelemetryProcessingAlgorithm(inputSunsensor, inputVoltage, inputTemperature) {
    var outputBeta = {};  // This will store the derived values (you can modify as needed)

    // Process EPS telemetry for two channels (1 and 2)
    processEps(1, inputSunsensor, inputVoltage, inputTemperature, outputBeta);
    processEps(2, inputSunsensor, inputVoltage, inputTemperature, outputBeta);

    return outputBeta;  // Return the processed data
}

// Helper function to process EPS telemetry based on channel
function processEps(ch, inputSunsensor, inputVoltage, inputTemperature, outputBeta) {
    try {
        var epsData = convertEpsEq(inputSunsensor, inputVoltage, inputTemperature, ch);

        // Set the output values for voltage, current, and temperature
        outputBeta["channel" + ch] = epsData;  // Store values per channel
    } catch (error) {
        console.error("Error processing EPS data for channel " + ch + ": ", error);
    }
}


// Function to convert EPS data based on telemetry inputs and channel
function convertEpsEq(inputSunsensor, inputVoltage, inputTemperature, ch) {
    var voltage, current, temperature;

    // Example equations (modify as per your specific needs)
    if (ch === 1) {
        voltage = (0.521 * inputVoltage / 256 * 5) + 8.533;
        current = (inputVoltage * 5 / 256 - 1.6025) * 15;
        temperature = (1 / (1 / 298.15 - Math.log(10000 / (5 - 5 / 256 * inputTemperature)) / 4190)) - 273.15;
    } else if (ch === 2) {
        voltage = (1.034 * inputVoltage / 256 * 5) + 18.286;
        current = (inputVoltage * 5 / 256 - 1.6182) * 15;
        temperature = (1 / (1 / 298.15 - Math.log(10000 / (5 - 5 / 256 * inputTemperature)) / 4190)) - 273.15;
    }

    return {
        voltage: Math.round(voltage * 100) / 100,
        current: Math.round(current * 100) / 100,
        temperature: Math.round(temperature * 100) / 100
    };
}

// Process IMU data: Extract acceleration
function processIMU(telemetry) {
    try {
        return telemetry.imu('accel');
    } catch (error) {
        console.error("Error processing IMU data:", error);
        return null;
    }
}

// Process TVC data: Extract TVC-related telemetry
function processTVC(telemetry) {
    var tvcData = [];
    try {
        for (var i = 0; i < telemetry.tvc_tlm.tvc.length; i++) {
            var tvcValues = telemetry.tvc_tlm.tvc[i].fvalues();
            tvcData.push({
                current_actual_value: tvcValues[1],
                target_position: tvcValues[4],
                pos_demand_value: tvcValues[6]
            });
        }
    } catch (error) {
        console.error("Error processing TVC data:", error);
    }
    return tvcData;
}

// Process GPSR data: Convert ECEF to LLA
function processGPSR(telemetry) {
    try {
        var gpsr = telemetry.gpsr_data;
        var lla = convertECEFToLLA(gpsr.ecef[0], gpsr.ecef[1], gpsr.ecef[2]);
        return lla;
    } catch (error) {
        console.error("Error processing GPSR data:", error);
        return null;
    }
}

// Convert ECEF coordinates to Latitude, Longitude, Altitude (LLA)
function convertECEFToLLA(ecefX, ecefY, ecefZ) {
    try {
        // Placeholder function - needs proper ECEF to LLA conversion logic
        return [ecefX, ecefY, ecefZ];
    } catch (error) {
        console.error("Error in ECEF to LLA conversion:", error);
        return null;
    }
}

// Process EPS data for multiple channels
function processEPS(telemetry) {
    var epsData = [];
    var channels = [1, 2];

    try {
        for (var i = 0; i < channels.length; i++) {
            var epsValues = getEPSValues(telemetry, channels[i]);
            if (epsValues) {
                epsData.push(epsValues);
            }
        }
    } catch (error) {
        console.error("Error processing EPS data:", error);
    }

    return epsData;
}

// Helper function to get EPS values from telemetry for a specific channel
function getEPSValues(telemetry, ch) {
    try {
        var epsVoltage = telemetry.eps_tlm['VOPT' + ch];
        var epsCurrent = telemetry.eps_tlm['IOPT' + ch];
        var epsTemp = telemetry.eps_tlm['TMP' + ch];

        if (epsVoltage === undefined || epsCurrent === undefined || epsTemp === undefined) {
            throw new Error("Missing EPS data for channel " + ch);
        }

        return {
            voltage: epsVoltage,
            current: epsCurrent,
            temperature: epsTemp
        };
    } catch (error) {
        console.error("Error getting EPS values for channel " + ch + ": ", error);
        return null;
    }
}
