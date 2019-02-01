import binascii
import struct

class Serializer:
	def __init__(self, tx):
		self.serial = struct.pack('<I', tx.version).hex()
		self.serial = self.serial + struct.pack('B', tx.get_input_counter()).hex()
		self.serial = self.serial + self.serialize_input(tx.inputs.copy())
		self.serial = self.serial + struct.pack('B', tx.get_output_counter()).hex()
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
		
		inputs, serializer = self.deserialize_input(input_counter, count_b_input, serializer)
		self.ret['Inputs'] = inputs

		output_counter, count_b_output = self.calc_var_int(0, serializer)
		self.ret['Output Count'] = output_counter
		
		outputs, serializer = self.deserialize_output(output_counter, count_b_output, serializer)
		self.ret['Outputs'] = outputs
		self.ret['Locktime'] = struct.unpack("<I", binascii.unhexlify(serializer))[0]	

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
			serial = serial[(var_int * 2) :]
			d_input['Sequence'] = struct.unpack('<I', binascii.unhexlify(serial[:8]))[0]
			serial = serial[8:]	
			input_counter -= 1
			inputs.append(d_input)
		#print(inputs)
		return inputs, serial

	def deserialize_output(self, output_counter, count_b_output, serializer):
		serial = serializer[count_b_output :]
		outputs = []
	
		while output_counter > 0:
			d_output = {}
			d_output['Value'] = struct.unpack('<Q', binascii.unhexlify(serial[:16]))[0]
			
			var_int, count_byte = self.calc_var_int(16, serial)
			serial = serial[(16 + count_byte) : ]
			d_output['ScriptPubKey Size'] = hex(var_int)[2:]
			d_output['ScriptPubKey'] = serial[: (var_int * 2)]
			serial = serial[(var_int * 2) :]
			
			output_counter -= 1
			outputs.append(d_output)
		
		#print(outputs)
		return outputs, serial

	def get_deserializer(self):
		return self.ret


#deser = Deserializer("01000000018190374a5a1feb54fab4417fac1a3d9185de06fd8dcac34822c7cd00083638b1000000006b483045022100b73d2ef337b0733c99ddd0c66a361ab003fc628a4a8667f7b36024e15f00974402203ea2712c0d764aa79cd283e65e5385d5da4b6b35e2b06548e2cd208bc3571d8b012103c13dca192f1ba64265d8efca97d43b822ff24db357c13b0e6e0395cf91e9efaeffffffff0250da1100000000001976a9140964c6feb963ade6836e722670abbc0147ca5cec88ac00e20400000000001976a914977ae6e32349b99b72196cb62b5ef37329ed81b488ac00000000")
#print(deser.get_deserializer())
