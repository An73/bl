import secrets
import struct
import binascii
import hashlib
import hmac
from bitstring import BitArray


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
	#print(dictionary)
	mnemonic = []
	for entr in entropy12:
		mnemonic.append(dictionary[entr])
		#print(entr)
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
	#print(numb)
	bits = []
	s = ''
	for n in numb:
		#print(n)
		#bits.append(BitArray(hex=(struct.pack('>H', n)).hex()).bin[5:])
		s += BitArray(hex=(struct.pack('>H', n)).hex()).bin[5:]

	#print(BitArray(hex=(struct.pack('>H', numb[0])).hex()).bin)
		
	print(hashlib.sha256(BitArray(s)).hexdigest())
	return int(s, 2)

def get_master_node(entropy):
	return hmac.new(bytes(entropy), msg='Bitcoin seed'.encode('utf-8'), digestmod=hashlib.sha512)



#import hmac
#import hashlib
#import base64
#dig = hmac.new(b'1234567890', msg=your_bytes_string, digestmod=hashlib.sha256).digest()
#base64.b64encode(dig).decode()

#print(get_mnemonic())
print(get_secrets_from_mnemonic(['salmon', 'evoke', 'track', 'embody', 'sibling', 'celery', 'parrot', 'neck', 'bus', 'visual', 'acquire', 'fabric']))
print(get_master_node(1082763))
#print(struct.unpack("<L", byte))
4049639642424071766793045316491381082763
