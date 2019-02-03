

def send(address, amount):
	prev_txid_utxo = "486c887f2378feb1ea3cdc054cb7b6722e632ab1edac962a00723ea0240f2e9c"
	privkey = "a5a89635770334177bcfa2da572dfc5d940484be73c6b20daccc4d6c397cd695"

	hash_pubkey = bare58check.b58decode(bytes(address, "utf-8"))
	hash_pubkey = hash_pubkey[1:-4].hex()

	public = wallet.public_to_compressed(wallet.get_public_key(binascii.unhexlify(privkey)))
	
	tr = transaction.Transaction(0)
	tr.add_output(35, hash_pubkey)
	tr.add_input(prev_txid_utxo, 1, "", public)
	message = tr.get_txid()
##PART2	
	signature, public = wallet.sign(privkey, message)
	tr = transaction.Transaction(0)
	tr.add_output(35, hash_pubkey)
	tr.add_input(prev_txid_utxo, 1, signature, public)


	
