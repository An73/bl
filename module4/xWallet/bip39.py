import secrets
import struct


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
	
	return numb




#import hmac
#import hashlib
#import base64
#dig = hmac.new(b'1234567890', msg=your_bytes_string, digestmod=hashlib.sha256).digest()
#base64.b64encode(dig).decode()

#print(get_mnemonic())
print(get_secrets_from_mnemonic(['much', 'evoke', 'track', 'embody', 'sibling', 'celery', 'parrot', 'neck', 'bus', 'visual', 'acquire', 'fabric']))

#print(struct.unpack("<L", byte))
