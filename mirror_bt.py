import bluetooth as bt
import time

def get_avail():
	return bt.discover_devices(lookup_names=True)

def connect(mac_addr):
	port = 1
	socket = bt.BluetoothSocket(bt.RFCOMM)
	socket.connect((mac_addr, port))
	return socket

def send(bt_socket, msg):
	bt_socket.send('2'.encode())

mac_addr = "98:D3:32:10:F8:FD"

# bt_socket = connect(mac_addr)
# print(bt.find_service(address=mac_addr))
# print(get_avail())
# send(bt_socket, 0)
# bt_socket.close()


class BtStrip:
	def __init__(self, mac_address="98:D3:32:10:F8:FD"):
		self.mac_address = mac_address
		self.port = 1


	def get_devices(self):
		return bt.discover_devices(lookup_names=True)

	def toggle_plug(self, plug_num):
		socket = bt.BluetoothSocket(bt.RFCOMM)
		socket.connect((self.mac_address, self.port))
		socket.send(str(plug_num).encode())
		socket.close()
		time.sleep(2)

