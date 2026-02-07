# Comprehensive Modbus TCP Client

import logging
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

class ModbusTCPClient:
    """
    A comprehensive Modbus TCP client that provides caching and fast operations.
    """

    def __init__(self, host, port=502, timeout=3):
        self.client = ModbusTcpClient(host, port)
        self.timeout = timeout
        self.cache = {}  # Caching to store retrieved values
        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            self.client.connect()
            self.logger.info("Connected to Modbus server.")
        except Exception as e:
            self.logger.error(f"Error connecting to Modbus server: {str(e)}")

    def read_coils(self, address, count):
        """
        Read coil values and cache the result.
        """  
        cache_key = ("coils", address, count)

        if cache_key in self.cache:
            self.logger.info("Returning cached coil values.")
            return self.cache[cache_key]

        try:
            result = self.client.read_coils(address, count, unit=1)
            if not result.isError():
                self.cache[cache_key] = result.bits
                self.logger.info(f"Read coils: {result.bits}")
                return result.bits
            else:
                self.logger.error(f"Error reading coils: {result}")
        except ModbusIOException as e:
            self.logger.error(f"Modbus IO Exception: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error reading coils: {str(e)}")

    def write_coil(self, address, value):
        """
        Write a value to a single coil.
        """  
        try:
            result = self.client.write_coil(address, value, unit=1)
            if result.isError():
                self.logger.error(f"Error writing coil: {result}")
            else:
                self.logger.info(f"Successfully wrote value: {value} to coil at address: {address}")
                # Clear cache for this coil
                if ("coils", address, 1) in self.cache:
                    del self.cache[("coils", address, 1)]
        except ModbusIOException as e:
            self.logger.error(f"Modbus IO Exception: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error writing coil: {str(e)}")

    def close(self):
        self.client.close()
        self.logger.info("Connection closed.")
