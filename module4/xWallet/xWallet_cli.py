import cmd
import xWallet
from tinydb import TinyDB, Query
from termcolor import cprint

class xWalletCli(cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.db = TinyDB('wallet.json')

	#def do_new(self, line):
	#	"""new\n     Generate private and public key"""
	#	privkey = wallet.generate_private_key()
	#	address = wallet.get_address(privkey)
	#	f = open('./wallet/address', 'w')
	#	f.write(address + '\n')
	#	f.close()
	#	cprint("private key   : [" + privkey.hex() + "]", 'yellow')
	#	cprint("public address: [" + address + "]", 'green')

	def do_new_h(self, line):
		if (line != ''):
			try:
				numb_acc = int(line)
				mnemo = xWallet.get_mnemonic()
				#print(xWallet.get_secrets_from_mnemonic(mnemo))
				cprint("Your mnemonic phrase:", 'green')
				cprint(" ".join(mnemo), 'yellow')
				full = xWallet.get_master_node(xWallet.get_secrets_from_mnemonic(mnemo))
				xWallet.add_master_seed(xWallet.sha256_seed(mnemo), full[:64], full[64:])
				n = 0
				while (n < numb_acc):
					xWallet.add_account(xWallet.sha256_seed(mnemo), full[:64], full[64:])
					n += 1
			except SyntaxError:
				cprint("Wrong number of accounts", 'red')
		else:
			mnemo = xWallet.get_mnemonic()
			cprint("Your mnemonic phrase:", 'green')
			cprint(" ".join(mnemo), 'yellow')
			#print(type(xWallet.sha256_seed(mnemo)))
			full = xWallet.get_master_node(xWallet.get_secrets_from_mnemonic(mnemo))
			xWallet.add_master_seed(xWallet.sha256_seed(mnemo), full[:64], full[64:])

	def do_get_all(self, line):
		cprint("Enter seed phrase:", 'yellow')
		inp = input()
		seed = inp.split(' ')
		json_all = xWallet.get_all_master_node(seed)
		if json_all == []:
			return 
		cprint("Master Node", 'red')
		cprint('Pubkey: ' + json_all[0]['pubkey'], 'green')
		cprint('Chainkey: ' + json_all[0]['chainkey'], 'green')

		cprint('Accounts:', 'magenta')
		n = 0
		for acc in json_all[0]['accounts']:
			cprint('Number: ' + str(n), 'green')
			cprint('Pubkey: ' + acc['pubkey'], 'green')
			cprint('Chainkey: ' + acc['chainkey'], 'green')
			cprint('Wallet Chains:', 'yellow')
			k = 0
			for wc in acc['wallet_chain']:
				k = 0
				cprint('Number: ' + str(k), 'yellow')
				cprint('Pubkey: ' + wc['pubkey'], 'yellow')
				cprint('Chainkey: ' + wc['chainkey'], 'yellow')
				cprint('Address:', 'cyan')
				for add in wc['address']:
					cprint('[' + add + ']', 'cyan')

			n += 1

	def do_add_wallet_chain(self, line):
		cprint("Enter seed phrase:", 'yellow')
		inp = input()
		inp = inp.split(' ')
		cprint("Enter number account:", 'yellow')
		acc = input()
		xWallet.add_wallet_chain(xWallet.sha256_seed(inp), int(acc))




	def do_EOF(self, line):
		return True

if __name__ == '__main__':
	xWalletCli().cmdloop()

		