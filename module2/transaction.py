import hashlib
import wallet
import binascii
import base58check
from serializer import Serializer

class Input:
	def __init__(self, prev_txid, prev_index, signature, pubkey):
		self.prev_txid = prev_txid
		self.prev_index = prev_index
		self.sequence = 4294967294
		self.script_hex = hex(len(binascii.unhexlify(signature)) + 1)[2:] + signature + "01" + hex(len(binascii.unhexlify(pubkey)))[2:] + pubkey
		#print("script_hex ", self.script_hex)
		self.length_script = len(binascii.unhexlify(self.script_hex))
		
	def set_sequense(sequense):
		self.sequense = sequense

class Output:
	def __init__(self, amount, hash_pubkey):
		self.value = amount
		len_pub = hex(len(binascii.unhexlify(hash_pubkey)))[2:]
		#print("len_pub", len_pub)
		self.script_hex = "76a9" + len_pub +  hash_pubkey + "88ac"
		self.script = "OP_DUP OP_HASH160 " + hash_pubkey + " OP_EQUALVERIFY OP_CHECKSIG"
		#print(self.script_hex)
		self.length_script = len(binascii.unhexlify(self.script_hex))

class Transaction:
	def __init__(self, locktime):
		self.version = 1
		#self.sender = sender
		#self.recipient = recipient
		#self.amount = amount
		self.inputs = []
		self.outputs = []
		self.locktime = locktime

	def add_input(self, prev_txid, prev_index, signature, pubkey):
		self.inputs.append(Input(prev_txid, prev_index, signature, pubkey))

	def get_input_counter(self):
		return len(self.inputs)

	def add_output(self, amount, hash_pubkey):
		self.outputs.append(Output(amount, hash_pubkey))
		
	def get_output_counter(self):
		return len(self.outputs)

	#def set_locktime(self, locktime):
	#	self.locktime = locktime
	#def get_hash(self):
		
	
#	def hash_calculated(self):
#		to_hash = self.sender + self.recipient + str(self.amount)
#		return hashlib.sha256(bytes(to_hash, "utf-8")).hexdigest()
#	def add_signature(self, signature, pub_key):
#		self.signature = signature
#		self.pub_key = pub_key

class CoinbaseTransaction(Transaction):
	def __init__(self):
		f = open('minerkey', 'r')
		wif = f.read().splitlines()[0]
		self.privkey = wallet.wif_to_private_key(wif)
		f.close()
		#recipient = wallet.get_address(binascii.unhexlify(self.privkey))
		#print('Mining reward sent to ', recipient)
		f = open('address', 'r')
		recipient = f.read().splitlines()[0]
		f.close()
		hash_pubkey = base58check.b58decode(bytes(recipient, "utf-8"))
		hash_pubkey = hash_pubkey[1:-4].hex()
		#super().__init__("0"*34, recipient, 50)
		super().__init__(0)
		input_coinbase = Input('0'*64, 4294967295, "ff", "ff")
		input_coinbase.script_hex = "03ec59062f48616f4254432f53756e204368756e2059753a205a6875616e67205975616e2c2077696c6c20796f75206d61727279206d653f2f06fcc9cacc19c5f278560300"
		input_coinbase.length_script = 69
		self.inputs.append(input_coinbase)
		self.add_output(50, hash_pubkey)

#transaction = Transaction(0)
#transaction.add_input("ceb7b8458419da7fa406da5d63b19b5306a2afc8", 1, "84f3fa278d3097e8572729fc3a73d7a810282f63e8865f4c9114243894f427d9", "2ef50fbcd0b8d433bab7a77bdb99607dd8dfe0f5")
#transaction.add_output(10000, "ceb7b8458419da7fa406da5d63b19b5306a2afc8")
#transaction.add_output(123123, "2ef50fbcd0b8d433bab7a77bdb99607dd8dfe0f5")

#serializer = Serializer(transaction)
#print(serializer.get_serializer())
