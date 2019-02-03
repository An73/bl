import transaction
import wallet
import base58check
import serializer
import binascii

def send(address, amount):
	prev_txid_utxo = "e3763a75ec08dc84f37593cd0d1ca556c650ee36689b162b1426cc70e71de748"
	privkey = "9a4b3677a4dfc4371f1efecb526a73e4d02d2d5c98f3da4bc5bc5d5a18f5c93b"

	hash_pubkey = base58check.b58decode(bytes(address, "utf-8"))
	hash_pubkey = hash_pubkey[1:-4].hex()

	public = wallet.public_to_compressed(wallet.get_public_key(binascii.unhexlify(privkey)))
	print(public)	
	tr = transaction.Transaction(0)
	tr.add_output(35, hash_pubkey)
	tr.add_input(prev_txid_utxo, 1, "", public)
	message = tr.get_txid()
##PART2	
	signature, public = wallet.sign(privkey, message)
	tr = transaction.Transaction(0)
	tr.add_output(35, hash_pubkey)
	print(signature)
	tr.add_input(prev_txid_utxo, 1, signature.hex(), public)

	print(serializer.Serializer(tr).get_serializer())


send("13dWYCn6qCqKPwrqckfTmD3YSUUPT4Zasd", 10)


	
