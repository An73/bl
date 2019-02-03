import binascii
import hashlib

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
	pubkey = binascii.unhexlify(script_sig)[(len_ss + 1) : ]

	stack.append(signatura)
	stack.append(pubkey)

	if script_pub_key[:2] == "76" and script_pub_key[2:4] == "a9":
		stack.append(stack[-1])
		pop = stack.pop()
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
	print(hashpub_1)
	hashpub_2 = stack.pop()
	print(hashpub_2)
	if (hashpub_1 != hashpub_2):
		return False
	
	
	return check_signature(stack.pop(), stack.pop(), tr_des)
#	print(signatura.hex())
#	print(pubkey.hex())

print(P2PKH("47304402201961b3b4684421b6cbfe0f3ff6e74ba8fe5690eff5b3776c203e87911c9b74ab02205e9d030b436cc10eda5d2704cbba26bed97f952fd4599a6b06cba814a2dde7760121031bdc17c61896f1c90478c90b43f22eb16dee6fd114ec1e9417d66f415663fce9", "76a914701b43f864c5999e03b8f60c2784d411ed51aa4288ac"))
	
