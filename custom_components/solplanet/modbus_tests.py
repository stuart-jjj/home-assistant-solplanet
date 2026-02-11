import types
from unittest.mock import AsyncMock, Mock

import pytest

from . import coordinator as coord_mod
from .coordinator import SolplanetDataUpdateCoordinator
from .const import (
    CONF_MODBUS_HOST,
    CONF_MODBUS_PORT,
    CONF_MODBUS_SOC_ENABLED,
    CONF_MODBUS_SOC_REGISTER,
    CONF_MODBUS_UNIT_ID,
)


class DummyConfigEntry:
    def __init__(self, data, options=None):
        self.data = data
        self.options = options or {}


class DummyConfigEntries:
    def __init__(self, entry):
        self._entry = entry

    def async_get_entry(self, entry_id):
        return self._entry


class DummyHass:
    def __init__(self, entry):
        self.config_entries = DummyConfigEntries(entry)

    async def async_add_executor_job(self, func):
        return func()


class DummyInv:
    def __init__(self, isn, is_storage=False, rate=10000, type_=1, mod_r=1):
        self.isn = isn
        self._is_storage = is_storage
        self.rate = rate
        self.type = type_
        self.mod_r = mod_r

    def isStorage(self):
        return self._is_storage


class DummyBatteryData:
    def __init__(self, soc):
        self.soc = soc
        self.soc_source = None


def _build_api():
    api = Mock()
    api.version = "v1"
    api.get_inverter_info = AsyncMock(
        return_value=types.SimpleNamespace(inv=[DummyInv("inv1", is_storage=True)])
    )
    api.get_inverter_data = AsyncMock(return_value=types.SimpleNamespace())
    api.get_battery_data = AsyncMock(return_value=DummyBatteryData(10))
    api.get_battery_info = AsyncMock(return_value=types.SimpleNamespace(type=1, mod_r=1))
    api.get_schedule = AsyncMock(return_value={"raw": {}})
    api.modbus_read_holding_registers = AsyncMock(return_value=[1, 0, 0, 0])
    api.get_meter_data = AsyncMock(return_value=types.SimpleNamespace(tim="1"))
    api.get_meter_info = AsyncMock(return_value=types.SimpleNamespace(sn="m1"))
    return api


@pytest.mark.asyncio
async def test_read_modbus_soc_disabled_returns_none():
    entry = DummyConfigEntry(
        data={
            CONF_MODBUS_SOC_ENABLED: False,
            CONF_MODBUS_HOST: "1.2.3.4",
            CONF_MODBUS_PORT: 502,
            CONF_MODBUS_UNIT_ID: 1,
            CONF_MODBUS_SOC_REGISTER: 1,
        }
    )
    hass = DummyHass(entry)
    api = _build_api()
    coordinator = SolplanetDataUpdateCoordinator(hass, api, "entry1", 30)

    result = await coordinator._read_modbus_soc()

    assert result is None


@pytest.mark.asyncio
async def test_read_modbus_soc_enabled_success(monkeypatch):
    class DummyModbusClient:
        def __init__(self, host, port, auto_open=True):
            self.host = host
            self.port = port
            self.auto_open = auto_open
            self.unit_id = None

        def read_input_registers(self, register, count):
            return [80]

        def close(self):
            pass

    monkeypatch.setattr(coord_mod, "_MODBUS_AVAILABLE", True)
    monkeypatch.setattr(coord_mod, "ModbusClient", DummyModbusClient)

    entry = DummyConfigEntry(
        data={
            CONF_MODBUS_SOC_ENABLED: True,
            CONF_MODBUS_HOST: "1.2.3.4",
            CONF_MODBUS_PORT: 502,
            CONF_MODBUS_UNIT_ID: 3,
            CONF_MODBUS_SOC_REGISTER: 100,
        }
    )
    hass = DummyHass(entry)
    api = _build_api()
    coordinator = SolplanetDataUpdateCoordinator(hass, api, "entry1", 30)

    result = await coordinator._read_modbus_soc()

    assert result == 80


@pytest.mark.asyncio
async def test_read_modbus_soc_enabled_failure_returns_none(monkeypatch):
    class FailingModbusClient:
        def __init__(self, host, port, auto_open=True):
            self.unit_id = None

        def read_input_registers(self, register, count):
            raise RuntimeError("read failed")

        def close(self):
            pass

    monkeypatch.setattr(coord_mod, "_MODBUS_AVAILABLE", True)
    monkeypatch.setattr(coord_mod, "ModbusClient", FailingModbusClient)

    entry = DummyConfigEntry(
        data={
            CONF_MODBUS_SOC_ENABLED: True,
            CONF_MODBUS_HOST: "1.2.3.4",
            CONF_MODBUS_PORT: 502,
            CONF_MODBUS_UNIT_ID: 1,
            CONF_MODBUS_SOC_REGISTER: 1,
        }
    )
    hass = DummyHass(entry)
    api = _build_api()
    coordinator = SolplanetDataUpdateCoordinator(hass, api, "entry1", 30)

    result = await coordinator._read_modbus_soc()

    assert result is None


@pytest.mark.asyncio
async def test_async_update_data_soc_override_and_source(monkeypatch):
    entry = DummyConfigEntry(data={CONF_MODBUS_SOC_ENABLED: True})
    hass = DummyHass(entry)
    api = _build_api()
    coordinator = SolplanetDataUpdateCoordinator(hass, api, "entry1", 30)

    monkeypatch.setattr(coordinator, "_read_modbus_soc", AsyncMock(return_value=55))
    monkeypatch.setattr(coord_mod, "host", "1.2.3.4", raising=False)
    monkeypatch.setattr(coord_mod, "port", 502, raising=False)
    monkeypatch.setattr(coord_mod, "register", 1, raising=False)

    data = await coordinator._async_update_data()

    battery = next(iter(data["battery"].values()))
    assert battery["data"].soc == 55
    assert battery["data"].soc_source == "modbus"


@pytest.mark.asyncio
async def test_async_update_data_soc_source_http_when_no_override(monkeypatch):
    entry = DummyConfigEntry(data={CONF_MODBUS_SOC_ENABLED: True})
    hass = DummyHass(entry)
    api = _build_api()
    coordinator = SolplanetDataUpdateCoordinator(hass, api, "entry1", 30)

    monkeypatch.setattr(coordinator, "_read_modbus_soc", AsyncMock(return_value=None))

    data = await coordinator._async_update_data()

    battery = next(iter(data["battery"].values()))
    assert battery["data"].soc == 10
    assert battery["data"].soc_source == "http"
