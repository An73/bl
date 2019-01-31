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
		input_counter, count_b_input = self.calc_var_int(8, serializer)
		
		self.ret = {
			'Version' : struct.unpack("<I", binascii.unhexlify(serializer[:8]))[0],
			'Input Count' : input_counter
		}
		
		self.deserialize_input(input_counter, count_b_input, serializer)

	def calc_var_int(self, index, serializer):
		var_int = -1
		count_byte = -1

		if serializer[index : index + 2] == 'fd':
			var_int = struct.unpack('H', binascii.unhexlify(serializer[index + 2 : index + 6]))[0]
			count_byte = 6
		elif serializer[index : index + 2] == 'fe':
			var_int = struct.unpack('I', binascii.unhexlify(serializer[index + 2 : index + 8]))[0]
			count_byte = 8
		elif serializer[index : index + 2] == 'ff':
			var_int = struck.unpack('Q', binascii.unhexlify(serializer[index + 2 : index + 10]))[0]
			count_byte = 10
		else:
			var_int = struct.unpack('B', binascii.unhexlify(serializer[index : index + 2]))[0]
			count_byte = 2
		return var_int, count_byte

	def deserialize_input(self, input_counter, count_b_input, serializer):
		serial = serializer[8 + count_b_input :]
		inputs = []

		while input_counter > 0:
			d_input = {
				'TXID' : (binascii.unhexlify(serial[:64])[::-1]).hex(),
				'VOUT' : struct.unpack('<I', binascii.unhexlify(serial[64:72]))[0]
			}
			var_int, count_byte = self.calc_var_int(72, serial)
			serial = serial[(72 + count_byte) : ]
			d_input['ScriptSig Size'] = hex(var_int)[2:]
			d_input['ScriptSig'] = serial[: (var_int * 2)]
			serial = serial[(var_int) * 2 :]
			d_input['Sequence'] = struct.unpack('<I', binascii.unhexlify(serial[:8]))[0]
			serial = serial[8:]	
			input_counter -= 1
			inputs.append(d_input)
		#print(inputs)
		return inputs

	def get_deserializer(self):
		return self.ret


deser = Deserializer("01000000017967a5185e907a25225574544c31f7b059c1a191d65b53dcc1554d339c4f9efc010000006a47304402206a2eb16b7b92051d0fa38c133e67684ed064effada1d7f925c842da401d4f22702201f196b10e6e4b4a9fff948e5c5d71ec5da53e90529c8dbd122bff2b1d21dc8a90121039b7bcd0824b9a9164f7ba098408e63e5b7e3cf90835cceb19868f54f8961a825ffffffff014baf2100000000001976a914db4d1141d0048b1ed15839d0b7a4c488cd368b0e88ac00000000")

print(deser.get_deserializer())
