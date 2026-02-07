import socket

class ModbusTCPClient:
    def __init__(self, host, port=502):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            print(f"Connected to Modbus server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to Modbus server: {e}")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from Modbus server.")

    def read_holding_registers(self, address, count):
        if not self.client:
            print("Client is not connected.")
            return None
        try:
            request = self._build_read_request(address, count)
            self.client.sendall(request)
            response = self.client.recv(1024)
            return self._parse_response(response)
        except Exception as e:
            print(f"Failed to read holding registers: {e}")

    def _build_read_request(self, address, count):
        # Modbus read request construction
        transaction_id = 1
        protocol_id = 0
        length = 6
        function_code = 3
        return struct.pack('>HHHBBHH', transaction_id, protocol_id, length, 0x01, function_code, address, count)

    def _parse_response(self, response):
        if len(response) < 5:
            print("Invalid response received.")
            return None
        # Parse and return the response data
        return response[3:]  # example of returning just the data part

# Usage example:
# client = ModbusTCPClient("192.168.1.100")
# client.connect()
# data = client.read_holding_registers(0, 10)
# print(data)
# client.disconnect()