from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor

HOST = "10.129.6.191"
PORT = 1338

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

def send_to_server(input: str) -> tuple[str, str]:
    recvuntil("$ ")
    sendline(input)
    recvuntil("Encrypted Input (hex): ")
    inp_enc = recvline().strip()
    recvuntil("Encrypted Output (hex): ")
    outp_enc = recvline().strip()
    return (inp_enc, outp_enc)


# ===== YOUR CODE BELOW =====
############################################
_,togetlength = send_to_server("!flag")
flaglen = len(bytes.fromhex(togetlength))

plain = b"A"*(16*(10+10+10)+flaglen)
s1,s2 = send_to_server(plain.decode())

to_xor = strxor(plain[0:flaglen],bytes.fromhex(s1)[480:480+flaglen])

_,flag_enc = send_to_server("!flag")

byteflag = bytes.fromhex(flag_enc)
flag = strxor(byteflag,to_xor)

print(flag)

# ===== YOUR CODE ABOVE =====


target.close()
