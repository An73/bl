import hashlib

def get_merkle_root(merkle):
	while len(merkle) != 1:
		new_merkle = []
		if len(merkle) % 2 != 0:
			merkle.append(merkle[-1])
		for i, j in enumerate(merkle):
			merkle[i] = hashlib.sha256(j.encode('utf-8')).hexdigest()
		for i, j in enumerate(merkle):
			if (i + 1) % 2 == 0:
				new_merkle.append(k + j)
			k = j
		merkle = new_merkle
	return hashlib.sha256(merkle[0].encode('utf-8')).hexdigest()

