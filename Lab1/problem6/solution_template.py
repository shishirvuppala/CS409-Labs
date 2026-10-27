from pwn import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor

from Crypto.Cipher import AES

HOST = "10.129.6.191"
PORT = 1339

# Uncomment the 'process' line below when you want to test locally, uncomment the 'remote' line below when you want to execute your exploit on the server
#target = process(["python", "./server.py"])
target = remote(HOST, PORT)

def recvuntil(msg):
    resp = target.recvuntil(msg.encode()).decode()
    print(resp)
    return resp

def sendline(msg):
    print(msg)
    target.sendline(msg.encode())

def recvline():
    resp = target.recvline().decode()
    print(resp)
    return resp

def recvall():
    resp = target.recvall().decode()
    print(resp)
    return resp


recvuntil("IV: ")
IV = bytes.fromhex(recvline())

recvuntil("Flag: ")
flag_enc = bytes.fromhex(recvline())


def validate_padding(iv_hex: str, ciphertext_hex: str) -> bool:
    recvuntil("validated:\n")
    sendline(ciphertext_hex)
    recvuntil("IV:\n")
    sendline(iv_hex)
    response = recvline()
    valid_padding = ("Valid Padding!" in response)
    return valid_padding


# ===== YOUR CODE BELOW =====
# The variable IV has the iv (as a bytes object)
# The variable flag_enc has the ciphertext (as a bytes object)
# You can call the function validate_padding(iv_hex: str, ciphertext_hex: str) -> bool which takes in the hex of the iv (str) and hex of the ciphertext (str) and returns True if the corresponding plaintext has valid padding, and return False otherwise (as dictated by the server's response)

chunksize = AES.block_size

def validate_padding_with_iv(ciphertext):
    return validate_padding(IV.hex(),ciphertext.hex())

def decrypt_block(cur_chunk: bytes, prev_chunk: bytes):
    final = bytearray(chunksize)
    Cdash = bytearray(b"A" * chunksize)
    for i in range(chunksize-1,-1,-1):
        pad = chunksize - i
        for p in range(chunksize-1, i, -1):
            Cdash[p] = prev_chunk[p] ^ final[p] ^ pad
        found = False
        for by in range(256):
            Cdash[i] = by
            if validate_padding_with_iv(bytes(Cdash) + cur_chunk):
                if i == chunksize - 1:
                    test = bytearray(Cdash)
                    test[i - 1] ^= 1
                    if not validate_padding_with_iv(bytes(test) + cur_chunk):
                        continue
                final[i] = prev_chunk[i] ^ by ^ pad
                found = True
                break
        if not found:
            raise ValueError(f"No valid byte found at position {i}")
    return bytes(final)


chunks = [IV,] + [flag_enc[i:i+chunksize] for i in range(0,len(flag_enc),chunksize)]

flagblocks = []

for i in range(len(chunks)-1):
    flagblocks.append(decrypt_block(chunks[i+1],chunks[i]))

flag = b''.join(flagblocks)
print(unpad(flag, AES.block_size))

# ===== YOUR CODE BELOW =====

target.close()
