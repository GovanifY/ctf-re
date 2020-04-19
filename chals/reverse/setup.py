import hashlib

def rng():
    BUF_SIZE = 65536 
    sha2 = hashlib.sha256()

    with open("flag.txt", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha2.update(data)
    hash_final=bytes.fromhex(sha2.hexdigest())
    rng=hash_final[len(hash_final)-1]%256
    return rng

print("setting up chal")
print("rng is: %d" % (rng()))
