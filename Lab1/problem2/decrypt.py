

ciphers = []

with open("ciphers.dat","r") as f:
    for line in f:
        hexstring = line.strip()
        if hexstring:
            ciphers.append(bytes.fromhex(hexstring))

flag = bytes(len(ciphers[0]))

for c in ciphers:
    flag = bytes(a | b for a, b in zip(c, flag))


print(flag)