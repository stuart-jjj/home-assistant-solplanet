%% Mermaid diagram: Solplanet integration architecture

flowchart LR
  subgraph HA[Home Assistant]
    direction TB
    Init[Integration init (__init__.py)]
    Coordinator[SolplanetDataUpdateCoordinator]
    Entities[Platforms: sensor/number/switch/select/button/binary_sensor]
    Services[services.py / services.yaml]
  end

  subgraph Device[Solplanet Dongle / Inverter]
    direction TB
    Dongle[Dongle HTTP endpoints]
    Modbus[Modbus RTU (over fdbg.cgi)]
  end

  Init --> Coordinator
  Coordinator --> Entities
  Services --> Coordinator
  Coordinator -->|HTTP GET/POST| Dongle
  Coordinator -->|Modbus frames via client| Modbus
  Dongle -->|responses| Coordinator

  classDef box stroke:#333,stroke-width:1px,fill:#f8f8f8
  class HA,Device box
