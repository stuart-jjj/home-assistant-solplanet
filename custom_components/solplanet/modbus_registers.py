from dataclasses import dataclass
from enum import Enum

# Enums for categories
class RegisterCategory(Enum):
    INVERTER = 'Inverter'
    BATTERY = 'Battery'
    METER = 'Meter'
    CONTROL = 'Control'


@dataclass
class Register:
    address: int
    scale_factor: float
    unit: str
    category: RegisterCategory

# INPUT_REGISTERS definition starting from address 1000+
INPUT_REGISTERS = {
    'inverter_model': Register(1000, 1, 'String', RegisterCategory.INVERTER),
    'rated_power': Register(1028, 1, 'W', RegisterCategory.INVERTER),
    'working_hours': Register(1307, 1, 'Hours', RegisterCategory.INVERTER),
    'PV_voltage_1': Register(1350, 0.1, 'V', RegisterCategory.INVERTER),
    'PV_current_1': Register(1351, 0.01, 'A', RegisterCategory.INVERTER),
    'PV_voltage_2': Register(1352, 0.1, 'V', RegisterCategory.INVERTER),
    'PV_current_2': Register(1353, 0.01, 'A', RegisterCategory.INVERTER),
    'grid_voltage': Register(1358, 0.1, 'V', RegisterCategory.INVERTER),
    'grid_frequency': Register(1359, 0.01, 'Hz', RegisterCategory.INVERTER),
    'output_power': Register(1360, 1, 'W', RegisterCategory.INVERTER),
    'temperature': Register(1361, 0.1, '°C', RegisterCategory.INVERTER),
    'status': Register(1362, 1, 'Status', RegisterCategory.INVERTER),
    'error_code': Register(1363, 1, 'Error Code', RegisterCategory.INVERTER),
    'energy': Register(1370, 1, 'kWh', RegisterCategory.INVERTER),
    'energy_import': Register(1371, 1, 'kWh', RegisterCategory.INVERTER),
    'energy_export': Register(1372, 1, 'kWh', RegisterCategory.INVERTER),
    'battery_SOC': Register(1621, 1, '%', RegisterCategory.BATTERY),
    'battery_voltage': Register(1622, 0.1, 'V', RegisterCategory.BATTERY),
    'battery_current': Register(1623, 0.01, 'A', RegisterCategory.BATTERY),
    'battery_power': Register(1624, 1, 'W', RegisterCategory.BATTERY),
    'battery_temperature': Register(1625, 0.1, '°C', RegisterCategory.BATTERY),
    'battery_health': Register(1626, 1, 'Health', RegisterCategory.BATTERY),
    'meter_power': Register(1700, 1, 'W', RegisterCategory.METER),
    'meter_voltage': Register(1701, 0.1, 'V', RegisterCategory.METER),
    'meter_frequency': Register(1702, 0.01, 'Hz', RegisterCategory.METER),
    'import_energy': Register(1710, 1, 'kWh', RegisterCategory.METER),
    'export_energy': Register(1712, 1, 'kWh', RegisterCategory.METER),
}

# HOLDING_REGISTERS definition starting from address 40001+
HOLDING_REGISTERS = {
    'inverter_power_control': Register(40201, 1, 'W', RegisterCategory.CONTROL),
    'battery_power_control': Register(41501, 1, 'W', RegisterCategory.CONTROL),
    'sleep_enabled': Register(41502, 1, 'Status', RegisterCategory.CONTROL),
    'LED_color': Register(41503, 1, 'Color Code', RegisterCategory.CONTROL),
    'LED_brightness': Register(41504, 1, 'Brightness', RegisterCategory.CONTROL),
}