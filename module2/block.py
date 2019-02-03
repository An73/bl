import time
import pending_pool
import merkle
import hashlib
import transaction
import wallet
import serializer
import os, sys

class Block:
	def __init__(self, previous_hash):
		self.timestamp = int(time.time())
		self.previous_hash = previous_hash
		
		coinbase = transaction.CoinbaseTransaction()
		#signature, pub_key = wallet.sign(coinbase.privkey, coinbase.hash_calculated()) 
		#coinbase.add_signature(signature, pub_key)
		tx_coinbase = serializer.Serializer(coinbase).get_serializer()
		self.transactions = pending_pool.last_tx()
		if not self.validates():
			print("not valid tx in block")
			return
		self.transactions.append(tx_coinbase)
		self.nonce = 0
		self.merkle_root = merkle.get_merkle_root(self.transactions.copy())
		
		readFile = open("mempool")
		lines = readFile.readlines()
		readFile.close()
		w = open("mempool",'w')
		w.writelines([item for item in lines[:-3]])
		w.close()

	
	def get_hash(self):
		hash_str = str(self.timestamp) + str(self.nonce) + str(self.previous_hash) + self.merkle_root 
		hash_block = hashlib.sha256(bytes(hash_str, 'utf-8')).hexdigest()
		return hash_block
		
	def validates(self):
		for i in self.transactions:
			if not pending_pool.check_tx(i):
				return False
		return True
	
	def mine(self, cmpl):
		hash_block = self.get_hash()
		while(self.get_hash()[:cmpl] != cmpl*'0'):
			self.nonce += 1
			hash_block = self.get_hash()
		return self.nonce
			


