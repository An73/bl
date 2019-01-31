import binascii
import struct

class Serializer:
	def __init__(self, tx):
		self.serial = struct.pack('<I', tx.version).hex()
		self.serial = self.serial + struct.pack('H', tx.get_input_counter()).hex()
		self.serial = self.serial + self.serialize_input(tx.inputs.copy())
		self.serial = self.serial + struct.pack('H', tx.get_output_counter()).hex()
		self.serial = self.serial + self.serialize_output(tx.outputs.copy())
		self.serial = self.serial + struct.pack('<I', tx.locktime).hex()

	def serialize_input(self, inputs):
		serial = ""
		for i in inputs:
			serial = serial + binascii.unhexlify(i.prev_txid)[::-1].hex()
			serial = serial + struct.pack('<I', i.prev_index).hex()
			serial = serial + hex(i.length_script)[2:]
			serial = serial + i.script_hex
			serial = serial + struct.pack('<I', i.sequence).hex()
		return serial

	def serialize_output(self, outputs):
		serial = ""
		for i in outputs:
			serial = serial + struct.pack('<Q', i.value).hex()
			serial = serial + hex(i.length_script)[2:]
			serial = serial + i.script_hex
		return serial
	#def __init__(self, tx):
	#	self.serial = (4 - len(hex(tx.amount)[2:])) * '0' + hex(tx.amount)[2:]
	#	self.serial = self.serial + (35 - len(tx.sender)) * '0' + tx.sender
	#	self.serial = self.serial + (35 - len(tx.recipient)) * '0' + tx.recipient
	#	self.serial = self.serial + (128 - len(tx.pub_key[2:])) * '0' + tx.pub_key[2:]
	#	self.serial = self.serial + tx.signature.hex()
	#
	def get_serializer(self):
		return(self.serial)

class Deserializer:
	def __init__(self, serializer):
		self.ret = {
			'amount' : int("0x" + serializer[:4], 0),
			'sender' : serializer[4:39].lstrip('0'),
			'recipient' : serializer[39:74].lstrip('0'),
			'public_key' : '04' + serializer[74:202].lstrip('0'),
			'signature' : serializer[202:]
		}
	def get_deserializer(self):
		return self.ret
			
