# Modbus TCP Implementation for Solplanet

## Overview
This Modbus TCP integration allows seamless communication with Solplanet devices. It supports reading and writing various data points, enabling a broad range of functionalities for monitoring and controlling devices through a standard protocol.

## New Modules
- **ModbusTCPClient**: Handles the connection and communication with Modbus TCP servers. Includes error handling and retry mechanisms.
- **ModbusDataManager**: Manages data retrieval and processing, allowing for easy access to device states and settings.
- **ModbusCommandExecutor**: Executes commands to the Modbus devices, ensuring that all operations are performed in the correct sequence.

## Performance Improvements
- Improved connection stability with automatic reconnection strategies.
- Reduced latency in data retrieval through optimized polling intervals.
- Enhanced error logging for easier debugging and support.

## Usage Examples
### Basic Configuration
To configure the Modbus TCP integration, add the following to your `configuration.yaml`:

```yaml
modbus:
  - name: "Solplanet"
    type: tcp
    host: "192.168.0.100"
    port: 502
    sensors:
      - name: "Solar Power"
        unit_of_measurement: "W"
        address: 100
        count: 1
```

### Reading Data
Once configured, you can access the solar power data in your Home Assistant dashboard, and it will update accordingly based on the defined polling intervals.

## Migration Guide
If you’re upgrading from a previous version of the Modbus integration, follow these steps to migrate your settings:
1. Backup your existing configuration files.
2. Replace any outdated module references in your configuration with those detailed in the New Modules section.
3. Review the performance settings and adjust as necessary based on the new capabilities.
4. Test your configuration using the Home Assistant configuration checker before restarting.

## Conclusion
This implementation of Modbus TCP is designed to enhance your experience with Solplanet devices, offering robust performance and ease of use. For any issues or enhancements, please feel free to contribute or raise issues in the repository.