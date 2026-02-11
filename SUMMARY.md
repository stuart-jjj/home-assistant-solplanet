# SUMMARY — Solplanet / VoltX Inverter Integration

Purpose

- Home Assistant custom integration to poll Solplanet/VoltX inverter dongles (V2-focused) and expose inverter, battery and meter data as entities.

High-level architecture

- `custom_components/solplanet/` — integration package.
- `SolplanetClient` (`client.py`) handles HTTP requests to the dongle and Modbus-over-HTTP frames.
- `api_adapter.py` adapts V1/V2 protocol differences and exposes high-level API methods.
- `coordinator.py` contains `SolplanetDataUpdateCoordinator` which periodically polls the device and stores structured data used by entities.
- Entity platforms: `sensor.py`, `switch.py`, `binary_sensor.py`, `number.py`, `select.py`, `button.py` — expose data and controls to Home Assistant.
- `services.yaml` + `services.py` provide integration-specific services (schedule, meter limits, modbus writes).

Key files (one-line responsibilities)

- `manifest.json` — integration metadata (domain, iot_class, version).
- `__init__.py` — config entry setup, device registration, platform forwarding.
- `client.py` — low-level HTTP client + Modbus helpers and helpers for battery schedules/modes.
- `api_adapter.py` — protocol wrapper selecting V1/V2 behaviors and higher-level API methods.
- `coordinator.py` — serializes polling, composes inverter/battery/meter payloads for entities.
- `entity.py` — base entity helpers used across platforms.
- `sensor.py` — defines sensor entities and mapping logic (units, value mappers).
- `switch.py` — implements power/control switches.
- `services.yaml` / `services.py` — user-invokable services (set/clear schedule, meter limits, modbus writes).
- `config_flow.py` — UI config entry flow for adding integration in Home Assistant.
- `modbus.py` — Modbus RTU framing/decoding helpers used by `client.py`.
- `const.py` — constants and lookups (error codes, identifiers).

Dependencies & runtime

- `manifest.json` declares `pyModbusTCP` in `requirements` for optional Modbus SoC / Modbus-over-TCP support (behind a feature toggle); core HTTP polling continues to rely on the Home Assistant runtime and its `aiohttp` client.
- Target runtime: Home Assistant (dev container provided). Use the dev container recommended in `docs/DEVELOPMENT.md`.

How the data flows (brief)

1. `SolplanetClient` performs HTTP GET/POST to the dongle endpoints and can encode/decode Modbus frames via `modbus.py`.
2. `SolplanetApiAdapter` interprets raw responses and exposes `get_inverter_info`, `get_inverter_data`, `get_battery_data`, `get_schedule`, etc.
3. `SolplanetDataUpdateCoordinator` calls adapter methods, aggregates payloads per inverter/battery/meter, and stores them in `coordinator.data`.
4. Entity platforms read from the coordinator to populate Home Assistant entities; services call API adapter/coordinator helper methods to perform actions.

Risk areas / fragile points

- Network reliability: dongles can be slow/unreliable; coordinator contains logic to mitigate flapping, but more tests would help.
- Modbus-over-HTTP: framing/decoding complexity and potential for incorrect writes — `services` include a `dry_run` flag for safety.
- Protocol differences between V1 and V2: `api_adapter.py` contains branching logic that should be validated against real devices.

Suggested starter issues (good first tasks)

1. Add unit tests for `modbus.py` frame generation/decoding (easy): tests for read/write frames and decode.
2. Add linter/formatting CI (medium): add `pyproject.toml` with `ruff`/`black` config and a simple GitHub Actions workflow.
3. Improve `client` error logging (easy): add more context on retries and include request URLs in debug logs.
