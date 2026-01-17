# Solplanet / VoltX Inverter Integration
[![hacs_badge](https://img.shields.io/badge/HACS-Integration-41BDF5.svg)](https://github.com/hacs/integration)
![GitHub all releases](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=Download%20Count&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.solplanet.total)
[![GitHub Release](https://img.shields.io/github/release/calvinbui/home-assistant-solplanet.svg)](https://github.com/calvinbui/home-assistant-solplanet/releases/)

![Solplanet-Logo-Gradient](https://github.com/user-attachments/assets/9675dcad-d32d-4605-972c-b3e244eb1ee8) \
This integration polls a local Solplanet-compatible inverter (including VoltX-branded devices) and exposes Inverter, Battery and Smart Meter information for Home Assistant.

This repository is a fork of the upstream integration by `zbigniewmotyka`, with a primary focus on **V2 devices/firmware**.

> [!Important]
> This fork does not aim to add new features or fixes for **V1**.

## Features
- Supports single- and three-phase inverters
- Sensors for inverter, battery and smart meter
- Battery mode control
- Battery schedule management (set/clear schedule slots)
- V2 meter “power limit control” (Limit power / Limit current / Zero power)
- Modbus RTU-over-HTTP (advanced service for writing holding registers)
- Designed to reduce device “flapping” (serialized polling + graceful degradation on timeouts)

## Protocol support
This integration automatically detects the protocol:

- **V1**: HTTP on port `8484`
- **V2**: HTTPS on port `443`

Different devices/firmwares expose different endpoints, so some features are V2-only.

## Installation

#### With HACS
[![Open in HACS.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=calvinbui&repository=home-assistant-solplanet&category=integration)

#### Manual installation
1. Place `solplanet` directory inside `config/custom_components` directory
2. Restart Home Assistant.

## Setting Up

1. Add Solplanet from the Integration page.
2. Enter the IP address of your Solplanet inverter
3. The integration will do the rest.

## Services / Actions
The integration exposes a number of services (Developer Tools → Actions).

### Battery schedule
- `solplanet.set_schedule_slots`: Add one schedule slot for a battery on a given day.
- `solplanet.clear_schedule`: Clear a day’s schedule (or all days).

### Meter power limit control (V2)
These services configure the inverter’s meter-based export control.

- `solplanet.set_meter_limit_power`
  - Enables **Limit power** mode.
  - Supports absolute (W) and percent (%) targets.

- `solplanet.set_meter_limit_current`
  - Enables **Limit current** mode.
  - `Setpoint offset (A)` is required.
  - `Communications loss current limit (A)` must be `<= Maximum export current limit (A)`.

- `solplanet.set_meter_zero_power`
  - Enables **Zero power** mode.

- `solplanet.disable_meter_power_limit`
  - Disables power limit control.

### Modbus (advanced)
- `solplanet.modbus_write_single_holding_register`
  - Writes a single Modbus holding register using the dongle’s Modbus RTU-over-HTTP bridge.
  - Intended for advanced users.

## Notes / Troubleshooting
- Home Assistant caches `services.yaml` descriptions. If you update this integration, a **full Home Assistant restart** may be required for the Actions UI to show the latest fields.
- Some devices are slow to respond. This integration prefers returning service success quickly and schedules a background refresh rather than blocking the UI.

## Home Assistant Energy Dashboard
Assign these sensors into the Energy Dashboard

|   **Section**    | **Home Assistant** |      **Solplanet**      |
|:----------------:|:------------------:|:-----------------------:|
|   Solar Panels   |  Solar Production  |     PV Energy Today     |
| Electricity Grid |  Grid Consumption  |  Grid Energy In Total   |
|                  |   Return to Grid   |  Grid Energy Out Total  |
| Battery Storage  |  Energy Incoming   |  Battery for Charging   |
|                  |  Energy Outgoing   | Battery for Discharging |

![386017334-b4899f13-82b7-4be4-938b-e5c2f0670adf](https://github.com/user-attachments/assets/c2660112-ad3b-4ee7-b6a6-5c73fb7f42bb)

> [!Tip]
> You may choose to define the tariff according to your local electrical utility service.

![image](https://github.com/user-attachments/assets/98e4db8e-88b6-4af7-b8b0-c5b6b2956530) ![image](https://github.com/user-attachments/assets/1a8c213a-e1aa-42b7-9614-6252eb378a0a)
