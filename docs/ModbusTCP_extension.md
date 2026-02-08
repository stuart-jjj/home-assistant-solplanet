# Modbus TCP Extension Plan

## Objective
Gradually refactor the existing Solplanet Home Assistant integration so that it can communicate directly with the inverter over Modbus/TCP (through the RS485-to-TCP gateway) while keeping the legacy HTTP/dongle stack intact until the Modbus path is proven.

## Target architecture
- **Home Assistant configuration** can host two paths simultaneously:
  1. **Legacy stack**: `SolplanetClient` → `SolplanetApiAdapter` → `SolplanetDataUpdateCoordinator` → platforms/services.
  2. **New Modbus stack**: `CoordinatorModbus` → `ModbusTCPClient` → `pymodbusTCP` → inverter (unit id 3).
- Entities should be able to read from either coordinator so the new entry can be enabled incrementally.
- Services and actions will eventually route through the Modbus client once parity is reached.

## Stage 0 – Foundation
1. **Add dependency**: declare `pymodbusTCP` in `custom_components/solplanet/manifest.json` so the new path can be installed.
2. **ModbusTCPClient** (`modbus_tcp_client.py`): wrap `pyModbusTCP.client.ModbusClient` with async-safe helpers for the registers you already validated (`1358`, `1307`, `1028`, `1621`).
3. **CoordinatorModbus** (`modbus_coordinator.py`): cache regular updates, expose `coordinator.data['modbus']`, and serialize update cycles similar to the existing coordinator.
4. **New entrypoint** (`modbus_entry.py`): register a Modbus-specific config entry tied to host/port/unit id, instantiate `CoordinatorModbus`, and forward a small set of sensors.

## Stage 1 – Parallel sensor coverage
1. **Sensor wiring**: update platforms so entities read from either legacy data or `coordinator.data.get('modbus')` (preferably keyed data so you can keep helpers reusable).
2. **Target sensors**: grid voltage, working hours, rated power, battery SOC (the ones proven in your test script).
3. **Docs**: explain how to add and run the Modbus config entry while keeping the legacy entry for fallback.

## Stage 2 – Feature expansion
1. **Register map expansion**: add inverter power (offset 200), battery more settings (offsets 1500–1503), etc., into the Modbus coordinator data structure.
2. **Entity control**: route setter methods like `set_inverter_power`, `set_battery_power`, schedule manipulation, etc., through `ModbusTCPClient` (possibly reusing the existing Modbus helper logic but triggered by the new coordinator).
3. **Services**: either refactor existing service handlers or create Modbus-specific variants once the Modbus data path supplies the necessary context.

## Stage 3 – Cutover & cleanup
1. **Switch default entry**: update `custom_components/solplanet/__init__.py` to prefer/only load the Modbus entry and document the HTTP path as legacy.
2. **Remove old layers**: retire `SolplanetClient`, `SolplanetApiAdapter`, and dongle-specific files once the Modbus path covers all functionality.
3. **Service/platform cleanup**: ensure `services.yaml` and platform code no longer reference HTTP endpoints unless needed for legacy compatibility.

## Checkpoints / tickets
- ✅ Stage 0: Modbus entrypoint exists, the coordinator can read the four verified registers, and data is available to new sensors.
- 🚧 Stage 1: Sensor entities for voltage/SOC/hours/rated power work through the Modbus entry and documentation is published.
- ⚙️ Stage 2: Additional registers and write operations (LED, sleep, inverter power) are supported via Modbus, and services route through the Modbus client.
- 🧹 Stage 3: Legacy HTTP/dongle stack is deprecated and eventually removed after manual verification.

## Testing & rollout strategy
- Deploy the new Modbus entry alongside the legacy integration so you can compare telemetry and fall back quickly.
- Each stage must remain testable in isolation: start with only the proven registers, then add new coverage gradually while keeping the existing code untouched.
- Log RTU frames from the new client to match your standalone usage and ensure timings/values align.

## Next action
Once the document is reviewed, we can begin Stage 0 by scaffolding the Modbus TCP client/coordinator and wiring in the first sensors.
