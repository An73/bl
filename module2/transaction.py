import hashlib
import wallet
import binascii

class Input:
	def __init__(self, prev_txid, prev_index, signature, pubkey):
		self.prev_txid = prev_txid
		self.prev_index = prev_index
		self.sequense = 4294967294
		self.script = signature + " " + pubkey
		self.script_hex
		self.length_script = len(binascii.unhexlify(self.script_hex))
		
	def set_sequense(sequense):
		self.sequense = sequense

class Output:
	def __init__(self, amount, hash_pubkey):
		self.value = amount
		self.script = "OP_DUP OP_HASH160 " + hash_bubkey + " OP_EQUALVERIFY OP_CHECKSIG"

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
		self.inputs.append(Input(prev_txid, prev_index))

	def get_input_counter(self):
		return len(inputs)

	def add_ouput(self, amount, hash_pubkey):
		self.ouputs.append(Output(amount, hash_pubkey))
		
	def get_output_counter(self):
		return len(outputs)

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

