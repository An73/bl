import hashlib
import binascii
import base58check
import ecdsa
import os
import secrets

def GetPubKey(pubkey, compressed=False):
	if compressed:
		if pubkey.point.y() & 1:
			key = '03' + '%064x' % pubkey.point.x()
		else:
			key = '02' + '%064x' % pubkey.point.x()
	else:
		key = '04' + \
		'%064x' % pubkey.point.x() + \
		'%064x' % pubkey.point.y()

	return key	

def privkey_to_wif():
	f = open('privkey')
	privkey = f.read().splitlines()[0]
	f.close()
	#print("1--> " + privkey)
	privkey = wif = "80" + privkey
	#print("2--> " + privkey)
	privkey = hashlib.sha256(binascii.unhexlify(privkey)).hexdigest()
	#print("3--> " + privkey)
	privkey = hashlib.sha256(binascii.unhexlify(privkey)).hexdigest()
	#print("4--> " + privkey)
	privkey = bytes.fromhex(privkey)[0:4].hex()
	wif = wif + privkey
	#print("5--> " + wif)
	wif = base58check.b58encode(bytes.fromhex(wif))
	#print("6--> " + wif.decode("ascii"))
	return wif.decode("ascii")
    

def generate_private_key():
	private_key = binascii.unhexlify(secrets.token_hex(32))
	return private_key

def wif_to_private_key(wif):
	if (len(wif) != 51):
		return "0"
	#print("1--> " + wif)
	wif = base58check.b58decode(bytes(wif, 'utf-8'))
	#print("2--> " + wif.hex())
	checksum1 = bytes.fromhex(wif.hex())[-4:].hex()
	privkey = bytes.fromhex(wif.hex())[1:-4].hex()
	#print("checksum1 = " + checksum1 + "\nprivkey = " + privkey)
	wif = bytes.fromhex(wif.hex())[0:-4].hex()
	wif = hashlib.sha256(binascii.unhexlify(wif)).hexdigest()
	#print("3--> " + wif)
	wif = hashlib.sha256(binascii.unhexlify(wif)).hexdigest()
	#print("4--> " + wif)
	checksum2 = bytes.fromhex(wif)[0:4].hex()
	if (checksum1 == checksum2):
		return privkey
	return "0"

def get_public_key(privkey):
	private = ecdsa.SigningKey.from_string(privkey, curve=ecdsa.SECP256k1)
	public = private.get_verifying_key()
	#K_compressed = GetPubKey(public.pubkey, True)
	return "04" + public.to_string().hex()

def public_to_compressed(pubkey):
	pubkey = binascii.unhexlify(pubkey[2:])
	pubkey = pubkey[: int(len(pubkey) / 2)]
	if pubkey[-1] % 2:
		pubkey = b'\x03' + pubkey
	else:
		pubkey = b'\x02' + pubkey
	return pubkey.hex()
	

def get_address(privkey):
	#privkey=binascii.unhexlify("18e14a7b6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321725")
	public = get_public_key(privkey)
	public = public_to_compressed(public)
	#print("1--> " + public)
	address = hashlib.sha256(binascii.unhexlify(public)).hexdigest()
	#print("2--> " + address)
	address = hashlib.new('ripemd160', binascii.unhexlify(address)).hexdigest()
	#print("3--> " + address)
	address = '00' + address
	#print("4--> " + address)
	first = hashlib.sha256(binascii.unhexlify(address)).hexdigest()
	#print("5--> " + first)
	first = hashlib.sha256(binascii.unhexlify(first)).hexdigest()
	#print("6--> " + first)
	first = bytes.fromhex(first)[0:4].hex()
	address = address + first
	#print("7--> " + address)
	address = base58check.b58encode(bytes.fromhex(address))
	#print("8--> " + address.decode("ascii"))
	return	address.decode("ascii")

def sign(privkey, message):
	try:
		singing_key = ecdsa.SigningKey.from_string(binascii.unhexlify(privkey), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
	except:
		return (-1, -1)
	signature = singing_key.sign(message.encode('utf-8'), hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
	public = public_to_compressed(get_public_key(binascii.unhexlify(privkey)))
	return (signature, public)

#print(get_address("123"))
