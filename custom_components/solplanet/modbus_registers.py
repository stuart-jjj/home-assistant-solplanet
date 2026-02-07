# Solplanet Modbus Registers Mapping

# Comprehensive register mapping for Solplanet inverters

## Input Registers (for monitoring)

| Register Address | Name                     | Data Type      | Function                     |
|------------------|-------------------------|----------------|------------------------------|
| 0x0000           | Inverter Status         | 16-bit unsigned| Status of the inverter        |
| 0x0001           | Energy Production        | 32-bit unsigned| Cumulative energy produced   |
| 0x0002           | Grid Voltage            | 16-bit unsigned| Voltage of the grid          |
| 0x0003           | Grid Frequency          | 16-bit unsigned| Frequency of the grid        |
| 0x0004           | Inverter Temperature     | 16-bit unsigned| Temperature of the inverter   |

## Holding Registers (for control)

| Register Address | Name                     | Data Type      | Function                     |
|------------------|-------------------------|----------------|------------------------------|
| 0x0100           | Set Grid Voltage Limit  | 16-bit unsigned| Set voltage limit for grid   |
| 0x0101           | Enable/Disable Inverter  | 16-bit unsigned| 1 = Enable, 0 = Disable      |
| 0x0102           | Set Frequency Limit     | 16-bit unsigned| Set frequency limit          |
| 0x0103           | Reset Inverter          | 16-bit unsigned| 1 = Reset inverter           |