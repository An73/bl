import binascii
import struct
import array
import transaction
import serializer
import wallet
import hashlib
import base58check
#INPUT_TEST
#prev_txid = "84f3fa278d3097e8572729fc3a73d7a810282f63e8865f4c9114243894f427d9"
#prev_index = 1
#script_hex = "1600148ed2231a28bdde898dde4e83250a4bb33b1c5ac5"
#script_len = len(binascii.unhexlify(script_hex))
#sequence = 4294967294

#print(binascii.unhexlify(prev_txid)[::-1].hex())
#print(struct.pack('<I', prev_index).hex())
#print(hex(script_len)[2:])
#print(script_hex)
#print(struct.pack('<I', sequence).hex())

#amount = 6986172
#script_hex = "a914ceb7b8458419da7fa406da5d63b19b5306a2afc887"
#script_len = len(binascii.unhexlify(script_hex))


#print(struct.pack('<Q', amount).hex())
#print(hex(script_len)[2:])
#print(script_hex)

#TEST
check_address = base58check.b58decode(bytes("1BDmLvhKiqLwCkktnMPf3R8VBTma25Qmzv", "utf-8"))
check_address = check_address[1:-4].hex()
print("hash_pubkey ", check_address)


signature, public = wallet.sign("a5a89635770334177bcfa2da572dfc5d940484be73c6b20daccc4d6c397cd695", "bd8cbb719bb27ba5d6cbb0501dab110033b677fdffa3bdc4b2952ba67a87caab")

print("SIGNN ", signature.hex())
print("Public ", public)

tr = transaction.Transaction(0)
tr.add_input("486c887f2378feb1ea3cdc054cb7b6722e632ab1edac962a00723ea0240f2e9c", 1, signature.hex(), public)
tr.add_output(50, check_address)
print("txid", tr.get_txid())

serial = serializer.Serializer(tr)
print(serial.get_serializer())
print(serializer.Deserializer(serial.get_serializer()).get_deserializer())
#TEST

#cb = transaction.CoinbaseTransaction()
#serial = serializer.Serializer(cb)
#print(serial.get_serializer())







