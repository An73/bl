from tinydb import TinyDB, Query
from block_validator import block_validator
import block
import transaction
import requests

class Blockchain:
	def __init__(self):
		self.node = []
		self.compl = 2
		self.db = TinyDB('chain.json')
		try:
			f = open('config', 'r')
			self.config = f.read().splitlines()
			self.this_node = self.config[0]
			self.node = self.config[1:]
		except IOError:
			print('there must be a config')
			returnza
		if self.this_node == "":
			print('the first line should be equal to this node')
			return
	
	def mine(self):
		previous_block = self.db.all()[-1]
		new_block = block.Block(previous_block['hash_block'])
		new_block.mine(self.compl)
		self.add_block(new_block)
		print('New block created')
	
	def genesis_block(self):
		self.db.purge()
		#transaction.CoinbaseTransaction()
		genesis_block = block.Block(0)
		self.add_block(genesis_block)
	
	def add_node(self, node):
		self.node.append(node)
		f = open('config', 'a')
		f.write(node + '\n')
		f.close()

	def is_valid_chain(self, chain):
		for element in chain:
			if not block_validator(element):
				return False
		return True

	def resol_conflicts(self):
		len_chain = len(self.db.all())
		for i in self.node:
			try:
				r_lenght = requests.post('http://' + i + '/chain/length/')
				r_chain = requests.post('http://' + i + '/chain/')
			except:
				print("Error connect")
				return
			if (r_lenght.status_code == 200):
				len_node = r_lenght.json()['len_chain']
				chain_node = r_chain.json()
				if len_node > len_chain and self.is_valid_chain(chain_node):
					self.db.purge()
					for elem in chain_node:
						self.db.insert(elem)

	def submit_tx(self, transaction):
		try:
			r = requests.post('http://' + self.this_node + '/transaction/new/', data={'tx' : transaction})
		except:
			return False
		if r.status_code == 200:
			return True
		return False
		
	
	def add_block(self, block):
		self.db.insert({'timestamp': block.timestamp, 
				'previous_hash': block.previous_hash,
				'transactions': block.transactions,
				'nonce': block.nonce,
				'merkle_root': block.merkle_root,
				'hash_block': block.get_hash()})


bl = Blockchain()
bl.genesis_block()
