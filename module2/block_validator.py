import merkle
import hashlib

def block_validator(block):
	hash_str = str(block['timestamp']) + str(block['nonce']) + str(block['previous_hash']) + block['merkle_root']
	hash_check = hashlib.sha256(bytes(hash_str, 'utf-8')).hexdigest()
	if hash_check != block['hash_block']:
		return False
	merkle_root = merkle.get_merkle_root(block['transactions'].copy())
	if merkle_root != block['merkle_root']:
		return False
	return True
