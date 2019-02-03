import binascii
import hashlib
import transaction
import serializer
from tinydb import TinyDB

class Stack:
	def __init__(self):
		self.stack = []
	def push(self, var):
		self.stack.append(var)
	def pop(self):
		return self.stack.pop()
	def isEmpty(sefl):
		if self.stack == []:
			return True
		return False

def check_signature(pub_key, signatura, tr_des):
	tr = transaction.Transaction(0)
	for out in tr_des['Outputs']:
		tr.add_output(out['Value'], out['ScriptPubKey'][6:-4])
	for inp in tr_des['Inputs']:
		tr.add_input(inp['TXID'], inp['VOUT'], "", pub_key)
	message = tr.get_txid()

	vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pub_key), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
	try:
		vk.verify(signature, message)
	except ecdsa.BadSignatureError:
		return False
	return True

def P2PKH(script_sig, script_pub_key, tr_des):
	stack = []	

	len_ss = int(script_sig[:2], 16)
	signatura = binascii.unhexlify(script_sig)[1 : len_ss]
	pubkey = binascii.unhexlify(script_sig)[(len_ss + 2) : ]
	print(pubkey.hex())
	stack.append(signatura)
	stack.append(pubkey)

	if script_pub_key[:2] == "76" and script_pub_key[2:4] == "a9":
		stack.append(stack[-1])
		pop = stack.pop()
		print('pop ', pop)
		pop = hashlib.sha256(pop).hexdigest()
		pop = hashlib.new('ripemd160', binascii.unhexlify(pop)).hexdigest()
		stack.append(pop)
		len_hp = int(script_pub_key[4:6], 16)
		print(binascii.unhexlify(script_pub_key)[3 : (len_hp + 3)].hex())
		stack.append(binascii.unhexlify(script_pub_key)[3 : (len_hp + 3)].hex())
		if binascii.unhexlify(script_pub_key)[len_hp + 3 :].hex() != "88ac":
			return False
	else:
		return False
	
	hashpub_1 = stack.pop()
	print("h_1 ", hashpub_1)
	hashpub_2 = stack.pop()
	print("h_2 ", hashpub_2)
	if (hashpub_1 != hashpub_2):
		return False
	
	
	return check_signature(stack.pop(), stack.pop(), tr_des)
#	print(signatura.hex())
#	print(pubkey.hex())

def get_txid(tx):
	txid = hashlib.sha256(binascii.unhexlify(tx)).hexdigest()
	txid = hashlib.sha256(binascii.unhexlify(txid)).hexdigest()
	return txid

def check_tx(tx):
	deser = serializer.Deserializer(tx).get_deserializer()
	if deser['Inputs'][0]['TXID'] == '0'*64:
		return True
	db = TinyDB('chain.json')
	chain = db.all()
	for block in chain:
		for tr in block['transactions']:
			if get_txid(tr) == deser['Inputs'][0]['TXID']:
				locking = serializer.Deserializer(tr).get_deserializer()
				locking = locking['Outputs'][deser['Inputs'][0]['VOUT'] - 1]['ScriptPubKey']
				return P2PKH(deser['Inputs'][0]['ScriptSig'], locking, deser)
	
	return False

print(get_txid("01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff4503ec59062f48616f4254432f53756e204368756e2059753a205a6875616e67205975616e2c2077696c6c20796f75206d61727279206d653f2f06fcc9cacc19c5f278560300feffffff0132000000000000001976a9141cd7e21d457db71f56b59d9399c224b3d4fb66b888ac00000000"))

print(check_tx("010000000148e71de770cc26142b169b6836ee50c656a51c0dcd9375f384dc08ec753a76e3010000006b483045022100bbff2168b2f4729b9be904ae962fcabaf1564a12429d8bea44fa504a79a91d6d022030322c6907310c548c10ddeb7efa568ae83b2ce24e5ea2030a6fa8e02b8bd13c012102dcb71a40106b61b0fba3507e78d0f4fee2a119e0916b24ec3dac3171d3f7093cfeffffff0123000000000000001976a9141cd7e21d457db71f56b59d9399c224b3d4fb66b888ac00000000"))
