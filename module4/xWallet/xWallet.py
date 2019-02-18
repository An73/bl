import secrets
import struct
import binascii
import hashlib
import hmac
from bitstring import BitArray
from tinydb import TinyDB, Query, where


def get_mnemonic():
	i = 0
	entropy12 = []
	while i < 12:
		secret = secrets.randbelow(2048)
		entropy12.append(secret)
		i += 1
	f = open('dictionary')
	dictionary = f.read().splitlines()
	f.close()
	mnemonic = []
	for entr in entropy12:
		mnemonic.append(dictionary[entr])
	return mnemonic


def get_secrets_from_mnemonic(mnemonic):
	f = open('dictionary')
	dictionary = f.read().splitlines()
	f.close()

	numb = []
	for m in mnemonic:
		i = 0
		for d in dictionary:
			if d == m:
				numb.append(i)
				break
			else:
				i += 1
	bits = []
	s = ''
	for n in numb:
		s += BitArray(hex=(struct.pack('>H', n)).hex()).bin[5:]
	#print((4049639642424071766793045316491381082763 // 100).to_bytes(16, byteorder='big'))
	return int(s, 2)

def add_master_seed(sha256_seed, pubkey, chain):
	db = TinyDB('wallet.json')
	db.insert({'seed256' : sha256_seed,
				'pubkey' : pubkey,
				'chainkey' : chain,
				'accounts' : []})

def add_account(sha256_seed, pubkey, chain):
	db = TinyDB('wallet.json')
	ms = db.search(where('seed256') == sha256_seed)

	accounts = ms[0]['accounts']

	full = down(binascii.unhexlify(pubkey).hex(), chain, len(accounts))

	accounts.append({'wallet_chain' : [],
						'chainkey' : full[64:],
						'pubkey' : full[:64]})
	db.update({'accounts': accounts}, where('seed256') == sha256_seed)

def add_wallet_chain(sha256_seed, number_acc):
	db = TinyDB('wallet.json')
	acc = db.search(where('seed256') == sha256_seed)
	print(acc)
	acc = acc[0]['accounts']

	#print("12312312312 ", acc)
	full = down(acc[number_acc]['pubkey'], acc[number_acc]['chainkey'], len(acc))

	acc[number_acc]['wallet_chain'].append({'address' : [],
											'chainkey' : full[64:],
											'pubkey' : full[:64]})
	db.update({'accounts': acc}, where('seed256') == sha256_seed)

def get_all_master_node(mnemonic):
	db = TinyDB('wallet.json')
	secrets = sha256_seed(mnemonic)
	return db.search(where('seed256') == secrets)

def sha256_seed(mnemonic):
	f = open('dictionary')
	dictionary = f.read().splitlines()
	f.close()

	numb = []
	for m in mnemonic:
		i = 0
		for d in dictionary:
			if d == m:
				numb.append(i)
				break
			else:
				i += 1
	if len(numb) < 12:
		return 0
	sha256_s = 0
	for n in numb:
		sha256_s += n
	return hashlib.sha256(bytes(sha256_s)).hexdigest()

def get_master_node(entropy):
	return hmac.new(entropy.to_bytes(32, "big"), msg='Bitcoin seed'.encode('utf-8'), digestmod=hashlib.sha512).hexdigest()

def down(pubkey, chain, n):
	#print((int(chain, 16) | n).to_bytes(32, "big"))
	return hmac.new((int(pubkey, 16) | (n * 1234)).to_bytes(32, "big"), msg=chain.encode('utf-8'), digestmod=hashlib.sha512).hexdigest()

#q = get_master_node(get_secrets_from_mnemonic(get_mnemonic()))
#print(len(q))
#print(q)

