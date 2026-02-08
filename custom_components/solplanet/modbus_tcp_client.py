"""Modbus/TCP client wrapper using pyModbusTCP."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable

from pyModbusTCP.client import ModbusClient

_LOGGER = logging.getLogger(__name__)


class ModbusTCPClient:
    """Thin async wrapper around pyModbusTCP."""

    def __init__(self, host: str, port: int = 502, slave_id: int = 3, timeout: float = 3.0) -> None:
        self._client = ModbusClient(
            host=host,
            port=port,
            unit_id=slave_id,
            auto_open=True,
            auto_close=False,
            timeout=timeout,
        )
        self._host = host
        self._port = port
        self._slave_id = slave_id
        self._lock = asyncio.Lock()

    @property
    def slave_id(self) -> int:
        return self._slave_id

    async def read_input_registers(self, address: int, count: int = 1) -> list[int]:
        return await self._run_in_executor(self._client.read_input_registers, address, count)

    async def read_holding_registers(self, address: int, count: int = 1) -> list[int]:
        return await self._run_in_executor(self._client.read_holding_registers, address, count)

    async def write_single_register(self, address: int, value: int) -> bool:
        return await self._run_in_executor(self._client.write_single_register, address, value)

    async def close(self) -> None:
        await self._run_in_executor(self._client.close)

    async def _run_in_executor(self, func: Callable[..., Any], *args) -> Any:
        async with self._lock:
            return await asyncio.to_thread(self._execute, func, *args)

    def _execute(self, func: Callable[..., Any], *args):
        if func is self._client.close:
            return func(*args)

        if not self._client.is_open():
            if not self._client.open():
                raise ConnectionError(f"Failed to open Modbus connection to {self._host}:{self._port}")
        result = func(*args)
if result is None:
    raise ConnectionError(
        f"Modbus register read/write returned no data (host={self._host}, unit={self._slave_id})"
    )
return result