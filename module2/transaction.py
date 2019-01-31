import hashlib
import wallet
import binascii

from serializer import Serializer

class Input:
	def __init__(self, prev_txid, prev_index, signature, pubkey):
		self.prev_txid = prev_txid
		self.prev_index = prev_index
		self.sequence = 4294967294
		self.script_hex = hex(len(binascii.unhexlify(signature)))[2:] + signature + "01" + hex(len(binascii.unhexlify(pubkey)))[2:] + pubkey
		self.length_script = len(binascii.unhexlify(self.script_hex))
		
	def set_sequense(sequense):
		self.sequense = sequense

class Output:
	def __init__(self, amount, hash_pubkey):
		self.value = amount
		self.script_hex = "76a9" + hash_pubkey + "88ac"
		self.script = "OP_DUP OP_HASH160 " + hash_pubkey + " OP_EQUALVERIFY OP_CHECKSIG"
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
		super().__init__("0"*34, recipient, 50)

transaction = Transaction(0)
transaction.add_input("ceb7b8458419da7fa406da5d63b19b5306a2afc8", 1, "84f3fa278d3097e8572729fc3a73d7a810282f63e8865f4c9114243894f427d9", "2ef50fbcd0b8d433bab7a77bdb99607dd8dfe0f5")
transaction.add_output(10000, "ceb7b8458419da7fa406da5d63b19b5306a2afc8")
transaction.add_output(123123, "2ef50fbcd0b8d433bab7a77bdb99607dd8dfe0f5")

serializer = Serializer(transaction)
print(serializer.get_serializer())
