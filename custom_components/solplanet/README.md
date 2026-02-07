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
