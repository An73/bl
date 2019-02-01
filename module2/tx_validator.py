import hashlib
import base58check
import binascii
import ecdsa

def avail_addr(address):
	if 26 > len(address) or len(address) > 35:
		return False
	elif address[0] != '1' and address[0] != '3':
		return False
	check_address = base58check.b58decode(bytes(address, "utf-8"))
	check_sum = check_address[-4:].hex()
	check_address = check_address[:-4].hex()
	check_address = hashlib.sha256(binascii.unhexlify(check_address)).hexdigest()
	check_address = hashlib.sha256(binascii.unhexlify(check_address)).hexdigest()
	
	if (binascii.unhexlify(check_address)[:4].hex() != check_sum):
		return False
	return True

def verify_send_addr(check_address, pub_key):
	address = hashlib.sha256(binascii.unhexlify(pub_key)).hexdigest()
	address = hashlib.new('ripemd160', binascii.unhexlify(address)).hexdigest()
	address = '00' + address
	first = hashlib.sha256(binascii.unhexlify(address)).hexdigest()
	first = hashlib.sha256(binascii.unhexlify(first)).hexdigest()
	first = bytes.fromhex(first)[0:4].hex()
	address = address + first
	address = base58check.b58encode(bytes.fromhex(address)).decode("ascii")
	if (check_address == address):
		return True
	return False

def valid_signature(signature, pub_key, hash_tx):
	pub_key = pub_key[2:]
	vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pub_key), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
	try:
		vk.verify(signature, hash_tx.encode("utf-8"))
	except ecdsa.BadSignatureError:
		return False
	return True

