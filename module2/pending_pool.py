import binascii
from tx_validator import avail_addr, verify_send_addr, valid_signature
from transaction import Transaction
from serializer import Deserializer

def check_tx(serialized):
	deserialized = Deserializer(serialized)
	deserialized = deserialized.get_deserializer()
	tx_check = Transaction(deserialized.get('sender'), deserialized.get('recipient'), deserialized.get('amount'))
	tx_hash = tx_check.hash_calculated()
	if not avail_addr(deserialized.get('sender')) or not avail_addr(deserialized.get('recipient')):
		return False
	elif not verify_send_addr(deserialized.get('sender'), deserialized.get('public_key')):
		return False
	elif not valid_signature(binascii.unhexlify(deserialized.get('signature')), deserialized.get('public_key'), tx_hash):
		return False
	return True
	
def tx_to_mempool(serializer):
	f = open('mempool', 'a')
	f.write(serializer + '\n')
	f.close()

def last_tx():
	f = open('mempool', 'r')
	arr_tx = f.read().splitlines()
	if (len(arr_tx) < 4):
		return arr_tx
	else:
		return arr_tx[-3:]

