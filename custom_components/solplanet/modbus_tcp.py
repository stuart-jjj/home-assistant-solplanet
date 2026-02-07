import socket
import struct
import time

class ModbusTCPClient:
    def __init__(self, host, port=502):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def read_holding_registers(self, unit_id, address, count):
        transaction_id = int(time.time()) & 0xFFFF
        protocol_id = 0
        length = 6
        function_code = 3
        pdu = struct.pack('>BHH', unit_id, address, count)
        request = struct.pack('>HHHBB', transaction_id, protocol_id, length, function_code) + pdu

        self.socket.send(request)
        response = self.socket.recv(1024)
        return self.parse_response(response)

    def parse_response(self, response):
        transaction_id, protocol_id, length, unit_id, function_code = struct.unpack('>HHHBB', response[:8])
        if function_code == 3:
            byte_count = response[8]
            registers = struct.unpack('>' + 'H' * (byte_count // 2), response[9:9 + byte_count])
            return registers
        return None

if __name__ == '__main__':
    client = ModbusTCPClient('192.168.1.10')  # Replace with your Modbus server IP
    client.connect()
    try:
        print(client.read_holding_registers(1, 0, 10))  # Example usage
    finally:
        client.disconnect()