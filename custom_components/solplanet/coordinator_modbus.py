# Custom Modbus Coordinator

import asyncio
from pymodbus.client.async import AsyncModbusTCPClient

class CoordinatorModbus:
    def __init__(self, host, port=502):
        self.host = host
        self.port = port
        self.client = AsyncModbusTCPClient(self.host, port=self.port)

    async def connect(self):
        await self.client.connect()

    async def read_holding_registers(self, address, count=1):
        response = await self.client.read_holding_registers(address, count)
        if response.isError():
            raise Exception("Error reading registers")
        return response.registers

    async def close(self):
        await self.client.close()

# Example usage
async def main():
    coordinator = CoordinatorModbus('192.168.1.100')
    await coordinator.connect()
    try:
        registers = await coordinator.read_holding_registers(0, 10)
        print(registers)
    finally:
        await coordinator.close()

if __name__ == '__main__':
    asyncio.run(main())