# Enhanced Standalone Modbus TCP Dashboard

## Overview
This dashboard serves as an interface for monitoring and controlling Modbus TCP devices, including inverters, batteries, and meters. It provides real-time data display with capabilities for CSV logging.

## Features
- **Inverter Monitoring**: Display current power generation, efficiency, and status. Control functions to start, stop, and adjust settings.
- **Battery Monitoring**: Show battery status, charge level, and health. Allow control for charging modes and settings.
- **Meter Data Monitoring**: Display real-time energy consumption, voltage, and current measurements. 
- **CSV Logging**: Log data at configurable intervals for historical analysis.

## Implementation
```python
import modbus_tk
from modbus_tk import modbus_tcp
import csv
import time
import datetime

class ModbusTCPDashboard:
    def __init__(self, host, port):
        self.client = modbus_tcp.TcpMaster(host, port)
        self.client.set_timeout(5)

    def read_inverter(self):
        # Add logic to read inverter data
        pass

    def read_battery(self):
        # Add logic to read battery data
        pass

    def read_meter(self):
        # Add logic to read meter data
        pass

    def log_to_csv(self, data):
        with open('log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.datetime.now(), data])

if __name__ == '__main__':
    dashboard = ModbusTCPDashboard(host='192.168.1.100', port=502)
    while True:
        inverter_data = dashboard.read_inverter()
        battery_data = dashboard.read_battery()
        meter_data = dashboard.read_meter()
        dashboard.log_to_csv([inverter_data, battery_data, meter_data])
        time.sleep(60)  # Log every minute
```

## Usage
1. Configure the Modbus details (host and port).
2. Run the script to start monitoring and logging data.