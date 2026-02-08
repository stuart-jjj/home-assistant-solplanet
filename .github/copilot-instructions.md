# GitHub Copilot / AI Agent Instructions for home-assistant-solplanet

Purpose
- Help AI coding agents be immediately productive in this Home Assistant integration.

Big picture (short)
- This is a Home Assistant local_polling integration for Solplanet inverters: the HTTP client (`custom_components/solplanet/client.py`) talks to inverter dongles and the integration exposes sensors, switches, numbers, selects and services.
- Data flow: `SolplanetClient` -> `SolplanetApiAdapter` -> `SolplanetDataUpdateCoordinator` -> platform entities. Modbus operations use `fdbg.cgi` (see `ModbusApiMixin` in `client.py`).

Important patterns & conventions
- Async-first: use async functions and Home Assistant helper classes (DataUpdateCoordinator). See `custom_components/solplanet/coordinator.py`.
- Protocol variants: code supports `v1` and `v2` protocol modes. Many control operations (dongle, battery schedule, modbus writes) are V2-only and raise `NotImplementedError` for V1. Check `api.version` before calling V2 operations.
- Serialized updates: coordinator serializes update cycles with an asyncio.Lock to avoid concurrent dongle requests. Avoid concurrent fan-outs when adding features.
- Resilient payload handling: on transient failures the coordinator keeps previous payload sections rather than returning empty data — follow the same approach to reduce flapping.
- Modbus specifics: the project encodes Modbus RTU frames and posts them to `fdbg.cgi`. Register addresses are full Modbus addresses (e.g. 40001 + offset). Example: inverter power read uses register 40201 (offset 200). See `client.py` and `coordinator.py` for examples.

Modbus frame format & register map
- Frames: Modbus RTU frames are generated as a hex string and POSTed to `fdbg.cgi` with payload `{ "data": "<hex>" }` (see `client._send_modbus`). Frames are packed as:
	- Device ID (1 byte)
	- Function code (1 byte) — e.g. 0x03 read holding, 0x04 read input, 0x06 write single holding, 0x10 write multiple
	- Register offset / address or parameters (big-endian words as per Modbus)
	- CRC-16 (two bytes, little-endian) appended by the generator
	- The project uses `ModbusRtuFrameGenerator` in `custom_components/solplanet/modbus.py` to build and decode frames. It exposes `DataType` (B16,B32,S16,U16,S32,U32,E16,STRING) and `encode_request_data()` / `decode_response()` helpers.

- Dry-run: write helpers accept `dry_run=True` to return the generated RTU frame hex without sending it. Use this to inspect frames safely (see `ModbusApiMixin.modbus_write_*` and `SolplanetApiAdapter.modbus_write_*`).

Known register map (addresses are "full" Modbus addresses = 40001 + offset)
- Inverter power (switch):
	- Offset: 200 -> Register: 40001 + 200 = 40201
	- Device address used in code: 3
	- Type: U16
	- Read via Function 0x03 (holding registers); write via Function 0x06 (single) in code (1 = on, 0 = off).
- Battery "More Settings" (battery switches / LED / brightness):
	- Offsets: 1500..1503 -> Registers 41501..41504
		- 1500 (41501): Power (1 = on, 0 = shutdown)
		- 1501 (41502): Sleep flag (semantics: 0 = enabled, 1 = disabled)
		- 1502 (41503): LED color index (integer palette index)
		- 1503 (41504): LED brightness percent (0-100)
	- Device address used in code: 3
	- Read as a 4-register block (Function 0x03) and exposed in coordinator as `more_settings`.
	- Writes use Function 0x10 (write multiple registers) even for single-register writes — the official app behaves this way and the code mirrors it.

Notes on higher-level entities
- Many UI entities (numbers, selects, schedule slots) call coordinator/API helpers rather than write raw Modbus registers directly. Examples:
	- `soc_min` / `soc_max` call `coordinator.set_battery_soc_min` / `set_battery_soc_max` which delegate through `SolplanetApiAdapter` (V2-only).
	- Schedule slots use `BatterySchedule.encode_schedule()` and `set_schedule_slots()` which use the API's schedule endpoints rather than direct Modbus frames.

Quick examples
- Generate but do not send inverter power write frame (dry-run): call the adapter method with `dry_run=True` to see the RTU hex returned by the generator (see `SolplanetApiAdapter.modbus_write_single_holding_register`).

Concrete RTU examples
- The following are full Modbus RTU frames (hex) including CRC-16 (little-endian) generated with `ModbusRtuFrameGenerator` for device address 3 used in this integration:
	- Read inverter power (Read Holding Register offset 200 / register 40201, quantity=1):
		- Pre-CRC: `03 03 00 C8 00 01`
		- Full RTU hex (with CRC): `030300c800010416`
	- Write inverter power ON (Write Single Holding Register offset 200 / register 40201, value=1):
		- Pre-CRC: `03 06 00 C8 00 01`
		- Full RTU hex (with CRC): `030600c80001c816`
	- Read battery "More Settings" (Read Holding Registers offset 1500 / register 41501, quantity=4):
		- Pre-CRC: `03 03 05 DC 00 04`
		- Full RTU hex (with CRC): `030305dc000484dd`
	- Write battery "More Settings" (Write Multiple, offset 1500, quantity=1, value=1):
		- Pre-CRC: `03 10 05 DC 00 01 02 00 01` (function 0x10 header + byte count + register value)
		- Full RTU hex (with CRC): `031005dc000102000138ac`

How to generate dry-run frames
- Option A — offline using the bundled generator (recommended):
	From the repository root run a one-liner (Python 3):

	```bash
	python3 - <<'PY'
	from custom_components.solplanet.modbus import ModbusRtuFrameGenerator, DataType
	# Example: generate write single holding register (device=3, reg=40201, value=1)
	print(ModbusRtuFrameGenerator().generate_write_single_holding_register_frame(
			device_id=3, register_address=40201, value=1, data_type=DataType.U16
	))
	PY
	```

- Option B — from a running Home Assistant Python environment:
	- If you have a Python environment with access to the running `hass` object (developer shell, AppDaemon, or a custom helper), you can call the adapter with `dry_run=True` to get the frame hex without sending it. Example snippet to run inside an async context where `hass` is available:

	```py
	api = hass.data['solplanet'][<entry_id>]['api']
	# Async call; returns RTU hex when dry_run=True
	frame = await api.modbus_write_single_holding_register(
			data_type=DataType.U16,
			device_address=3,
			register_address=40201,
			value=1,
			dry_run=True,
	)
	print(frame)
	```

	- Note: obtaining `entry_id` and running arbitrary async code requires being inside Home Assistant runtime (e.g., an integration or an AppDaemon app). The offline generator in Option A is simpler for inspecting frames safely.


Key files to reference (examples)
- Integration entrypoints: [custom_components/solplanet/__init__.py](custom_components/solplanet/__init__.py#L1-L120)
- Coordinator & actions: [custom_components/solplanet/coordinator.py](custom_components/solplanet/coordinator.py#L1-L40)
- HTTP/Modbus client and helpers: [custom_components/solplanet/client.py](custom_components/solplanet/client.py#L1-L40)
- Services: [custom_components/solplanet/services.yaml](custom_components/solplanet/services.yaml)
- Package metadata: [custom_components/solplanet/manifest.json](custom_components/solplanet/manifest.json)

Developer workflows & commands
- Start Home Assistant using the repository VS Code task `Start Home Assistant` (task command: `supervisor_run`) when debugging the integration in a supervised environment.
- No automated tests are present in the repo; prefer manual validation by loading the integration in Home Assistant and exercising services declared in `services.yaml`.

Tips for edits and PRs
- Preserve async behavior and avoid blocking I/O on the event loop. Use HA helpers like `async_get_clientsession` and `DataUpdateCoordinator`.
- When adding write/control features, mirror existing error handling: catch transport/parsing errors, log debug details, and raise Home Assistant exceptions (`HomeAssistantError`, `UpdateFailed`) where appropriate.
- Keep device registry identifiers stable (see device creation in `__init__.py`) to avoid orphaned entities.

What not to change without checking
- The Modbus frame encoding/decoding (in `modbus.py` and `client.py`) — subtle bugs here can brick writes.
- Coordinator locking and refresh semantics — changing serialization can cause flapping/timeouts on real devices.

If something is unclear
- Ask for specific runtime details: whether you run Home Assistant supervised, in Docker, or in a dev container; testing instructions depend on that environment.

Please review — tell me any missing examples or developer commands to include.
