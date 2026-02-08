"""Sensors driven by the Modbus/TCP coordinator."""

from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_CONNECTION_METHOD,
    CONNECTION_METHOD_MODBUS,
    DOMAIN,
)
from .modbus_coordinator import ModbusDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ModbusSensorDescription(SensorEntityDescription):
    """Describe a Modbus sensor."""


SENSOR_DESCRIPTIONS: list[ModbusSensorDescription] = [
    ModbusSensorDescription(
        key="grid_voltage",
        name="Grid Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ModbusSensorDescription(
        key="battery_soc",
        name="Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ModbusSensorDescription(
        key="rated_power_kw",
        name="Rated Power",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ModbusSensorDescription(
        key="working_hours",
        name="Total Working Hours",
        native_unit_of_measurement=UnitOfTime.HOURS,
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
]


class ModbusSensor(CoordinatorEntity[ModbusDataUpdateCoordinator], SensorEntity):
    """Sensor backed by the Modbus coordinator."""

    entity_description: ModbusSensorDescription

    def __init__(self, coordinator: ModbusDataUpdateCoordinator, description: ModbusSensorDescription, entry_id: str) -> None:
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_name = description.name
        self._attr_unique_id = f"{entry_id}_{description.key}"

    @property
    def native_value(self) -> float | int | None:
        return self.coordinator.data.get(self.entity_description.key)


async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    if entry.data.get(CONF_CONNECTION_METHOD) != CONNECTION_METHOD_MODBUS:
        return

    coordinator: ModbusDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["modbus_coordinator"]

    async_add_entities(
        [
            ModbusSensor(coordinator, description, entry.entry_id)
            for description in SENSOR_DESCRIPTIONS
        ]
    , update_before_add=True)
