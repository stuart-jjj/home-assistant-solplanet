# DEV_SETUP — Solplanet Integration

This document describes how to set up a local development environment and common developer commands.

Quick: run in the provided Dev Container (recommended)

1. Open repository in VS Code.
2. Reopen in Container (Dev Containers) when prompted.
3. Start Home Assistant via the provided task: `Tasks: Run Task` → **Start Home Assistant**.
4. Home Assistant UI will be at: `http://localhost:7123` inside the dev container host mapping.

Manual / local Home Assistant testing (non-container)

- To test in a local Home Assistant installation, copy the integration folder into Home Assistant config:

```bash
# from repo root
cp -r custom_components/solplanet /path/to/homeassistant/config/custom_components/
# restart Home Assistant
```

Config / add integration

- In Home Assistant UI: Configuration → Integrations → Add Integration → search for "Solplanet" and follow prompts (enter dongle IP/host).

Developer convenience commands (run inside dev container)

- Open an interactive shell in the dev container (VS Code terminal) and run:

```bash
# Check Python version inside container
python -V

# Linting (suggested - install locally first)
python -m pip install ruff black
ruff check custom_components/solplanet
black --check custom_components/solplanet

# Run a quick grep for TODOs
rg "TODO|FIXME" custom_components/solplanet || true
```

Tests

- This repo currently has no test suite. Suggested next step: add unit tests for `modbus.py` and `client` helpers using `pytest`.

Safety notes

- Use `services.yaml` `dry_run` options before sending write requests to devices.
- When experimenting with `modbus_write_*` services, test with `dry_run: true` to validate frames.

Useful file locations

- Integration code: `custom_components/solplanet/`
- Developer guide: `docs/DEVELOPMENT.md`
- Integration metadata: `manifest.json`

TODO: add a basic `pyproject.toml` with `ruff`/`black` configuration and a simple GitHub Actions workflow to run linters on PRs.
