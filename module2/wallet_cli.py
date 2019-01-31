#!/usr/bin/env python3.6
import sys
import wallet
import binascii
import cmd
from tinydb import TinyDB, Query
from transaction import Transaction
from serializer import Serializer, Deserializer
import tx_validator
import blockchain

class WalletCli(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.db = TinyDB('chain.json')
		self.tx_send = []
		self.block_chain = blockchain.Blockchain()

	def do_new(self, line):
		"""new\n     Generate private and public key"""
		privkey = wallet.generate_private_key()
		address = wallet.get_address(privkey)
		f = open('address', 'w')
		f.write(address + '\n')
		f.close()
		print("private key   : [" + privkey.hex() + "]")
		print("public address: [" + address + "]")

	def do_import(self, path):
		"""import [/path/to/file]\n     Import a private key type WIF from a file with the command"""
		try:
			f = open(path, 'r')
			wif = f.read().splitlines()
			if not wif:
				print("file empty")
				return
			privkey = wallet.wif_to_private_key(wif[0])
			f.close()
			if privkey == "0":
				print("invalid wif key")
				return
			address = wallet.get_address(binascii.unhexlify(privkey))
			f =  open('address', 'w')
			f.write(address + '\n')
			f.close()
			print("private key   : [" + privkey + "]")
			print("public address: [" + address + "]")
		except FileNotFoundError:
			print("Not such file: '" + path + "'")
	
	def do_send(self, argv):	
		ar = argv.split()
		f = open('address', 'r')
		addresses = f.read().splitlines()
		if not addresses:
			print("*** Error addresses")
			return
		elif len(ar) < 2:
			print("*** Error argument")
			return	
		elif self.get_balance(addresses[0]) < int(ar[1]):
			print("Not enough money on balance")
			return
	
		priv_key = input("Enter private key: ")
		sender = addresses[0]
		transaction = Transaction(sender, ar[0], int(ar[1]))
		hash_t = transaction.hash_calculated()
		
		if (not tx_validator.avail_addr(transaction.sender) or not tx_validator.avail_addr(transaction.recipient)):
			print("*** Error addresses")
			return
		signature, pub_key = wallet.sign(priv_key, hash_t)
		if signature == -1 or pub_key == -1:
			print(" Error password")
			return
		if not tx_validator.verify_send_addr(sender, pub_key):
			print(" Error sender")
			return
		if not tx_validator.valid_signature(signature, pub_key, hash_t):
			print(" Error signature")
			return
		transaction.add_signature(signature, pub_key)
		serializer = Serializer(transaction).get_serializer()
		self.tx_send.append(serializer)
		print("Transactions for broadcast: ")
		print(self.tx_send)
	
	def do_broadcast(self, line):
		if not self.tx_send:
			print("No tranactions for broadcast")
			return
		for i in self.tx_send:
			if not self.block_chain.submit_tx(i):
				print("Broadcast failed, connection is missing")
				return
		print("Broadcast succsessfull")

	def get_balance(self, addr):
		balance = 0
		if addr == "":
			return -1
		db = TinyDB('chain.json')
		chain_json = self.db.all()
		for b in chain_json:
			for tx in b['transactions']:
				deserializer = Deserializer(tx)
				tx_check = deserializer.get_deserializer()
				if (tx_check['sender'] == addr):
					balance -= int(tx_check['amount'])
				elif (tx_check['recipient'] == addr):
					balance += int(tx_check['amount'])
		return balance

	def do_balance(self, addr):
		balance = self.get_balance(addr)
		if balance == -1:
			print('enter address')
		else:
			print("balance " + addr + ": " + str(balance))
	
	def do_EOF(self, line):
		return True

if __name__ == '__main__':
	WalletCli().cmdloop()

