# MODBUS Migration Guide

## 1. Overview of the Modbus TCP Refactoring
This document outlines the migration process from the HTTP API to the more efficient Modbus TCP. The refactoring aims to reduce latency and improve communication efficiency with the Solplanet devices.

## 2. Installation and Setup Instructions
1. Ensure you have the necessary dependencies installed:
   - Python 3.8+
   - pip
   - Required Python packages (check the requirements.txt)

2. Update your Home Assistant configuration to include the Solplanet Modbus driver.

3. Follow the installation process detailed in the [official installation guide](https://example.com/install).

## 3. Configuration Changes Needed
To switch from the HTTP API to Modbus TCP, modify your configuration as follows:
```yaml
solplanet:
  host: "192.168.1.100"
  port: 502
```
Make sure to remove any previous HTTP configurations related to Solplanet.

## 4. Performance Comparison
When tested, the Modbus TCP communication showed significant improvements in response times. Specifically:
- **HTTP API:** Response times often exceeded **30 seconds**.
- **Modbus TCP:** Average response time is approximately **<3 seconds**.

This substantial improvement can enhance real-time monitoring and control of your devices.

## 5. Testing and Verification Steps
1. After setup, verify the connection by using the following command:
   ```bash
   ping 192.168.1.100
   ```
2. Check the logs of Home Assistant for any warning or error messages.
3. Validate the data retrieval from the device by accessing the Solplanet integration in the Home Assistant dashboard.

## 6. Troubleshooting Guide
If you encounter issues:
- Check your network connection.
- Ensure the Modbus TCP settings are correct in your configuration.
- Review the Home Assistant logs for any clues.

## 7. Rollback Instructions
If you need to revert to the HTTP API:
1. Remove the Modbus TCP configurations from your configuration file.
2. Restore the old HTTP API configurations.
3. Restart Home Assistant to apply changes.

## 8. FAQ Section
- **Q: Why should I switch to Modbus TCP?**
  A: It offers faster response times and more reliable communication compared to the HTTP API.

- **Q: What if I experience connection issues?**
  A: Refer to the troubleshooting guide and ensure all configurations are correct.

- **Q: Is Modbus TCP supported on all Solplanet devices?**
  A: Yes, all recent models support Modbus TCP. Check your device documentation for more details.

---

This migration guide serves to support users through the transition to the improved Modbus TCP integration, ensuring a seamless and productive experience with Solplanet devices.