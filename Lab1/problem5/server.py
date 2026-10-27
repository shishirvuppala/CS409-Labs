from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

FLAG = b"REDACTED"

INCREMENT = 10
key = get_random_bytes(AES.block_size)
nonce = get_random_bytes(AES.block_size//2)

if __name__ == '__main__':
    ctr_val = 0
    print("Welcome to the Encrypted Echo Server!")
    print("Input \"!flag\" to have the flag sent to you.")

    while True:
        inp = input("\n$ ")
        outp = None
        if inp == "!flag":
            outp = FLAG
        else:
            outp = inp.encode()
        
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=ctr_val); ctr_val += INCREMENT
        inp_enc = cipher.encrypt(inp.encode()).hex()

        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce, initial_value=ctr_val); ctr_val += INCREMENT
        outp_enc = cipher.encrypt(outp).hex()

        print(f"Encrypted Input (hex): {inp_enc}")
        print(f"Encrypted Output (hex): {outp_enc}")
