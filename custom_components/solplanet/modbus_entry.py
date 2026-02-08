"""Helper entrypoint for Modbus/TCP configured entries."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry  # type: ignore[reportMissingImports]
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_CONNECTION_METHOD,
    CONF_HOST,
    CONF_INTERVAL,
    CONF_MODBUS_PORT,
    CONF_MODBUS_UNIT,
    CONNECTION_METHOD_MODBUS,
    DEFAULT_INTERVAL,
    DEFAULT_MODBUS_PORT,
    DEFAULT_MODBUS_UNIT,
    DOMAIN,
)
from .modbus_coordinator import ModbusDataUpdateCoordinator
from .modbus_tcp_client import ModbusTCPClient

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if entry.data.get(CONF_CONNECTION_METHOD) != CONNECTION_METHOD_MODBUS:
        return False

    port = entry.data.get(CONF_MODBUS_PORT, DEFAULT_MODBUS_PORT)
    unit = entry.data.get(CONF_MODBUS_UNIT, DEFAULT_MODBUS_UNIT)
    interval = entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL)

    client = ModbusTCPClient(host=entry.data[CONF_HOST], port=port, slave_id=unit)
    coordinator = ModbusDataUpdateCoordinator(hass=hass, client=client, update_interval=interval)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "modbus_coordinator": coordinator,
    }
    entry.runtime_data = {"modbus_coordinator": coordinator}

    _LOGGER.info("Initialized Modbus/TCP coordinator for %s", entry.title)

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    if entry.data.get(CONF_CONNECTION_METHOD) != CONNECTION_METHOD_MODBUS:
        return False

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if not unload_ok:
        return False

    coordinator: ModbusDataUpdateCoordinator | None = (
        hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).get("modbus_coordinator")
    )
    if coordinator is not None:
        await coordinator.async_close()

    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
