"""Coordinator for Modbus/TCP based data collection."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .modbus_tcp_client import ModbusTCPClient

_LOGGER = logging.getLogger(__name__)


class ModbusDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator that polls the inverter via Modbus/TCP."""

    def __init__(self, hass: HomeAssistant, client: ModbusTCPClient, update_interval: int) -> None:
        self._client = client
        self._update_interval = update_interval

        super().__init__(
            hass,
            _LOGGER,
            name="solplanet_modbus",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self) -> dict[str, float | int]:
        """Retrieve the verified register readings."""
        try:
            grid_voltage = (await self._client.read_input_registers(1358))[0] * 0.1
            working_hours = (await self._client.read_input_registers(1307))[0]
            rated_kw = (await self._client.read_input_registers(1028))[0] / 1000.0
            soc = (await self._client.read_input_registers(1621))[0]
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Modbus update failed", exc_info=True)
            raise UpdateFailed(f"Failed to poll Modbus registers: {err}") from err

        return {
            "grid_voltage": grid_voltage,
            "working_hours": working_hours,
            "rated_power_kw": rated_kw,
            "battery_soc": soc,
        }

    async def async_close(self) -> None:
        await self._client.close()
*** End of File