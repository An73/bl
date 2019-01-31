import binascii
import struct
import array

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

amount = 6986172
script_hex = "a914ceb7b8458419da7fa406da5d63b19b5306a2afc887"
script_len = len(binascii.unhexlify(script_hex))


print(struct.pack('<Q', amount).hex())
print(hex(script_len)[2:])
print(script_hex)
