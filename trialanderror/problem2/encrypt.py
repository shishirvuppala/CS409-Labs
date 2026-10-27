from Crypto.Random import get_random_bytes

def encrypt(message: str, key: bytes) -> str:
    msg_bytes = message.encode('utf-8')

    if len(key) < len(msg_bytes):
        raise ValueError(
            f"Key too short: need at least {len(msg_bytes)} bytes, got {len(key)}"
        )
    key = key[:len(msg_bytes)]

    encrypted_msg = bytes(a & b for a, b in zip(msg_bytes, key))

    return encrypted_msg.hex()

def generate_ciphers(message: str, n: int, filename: str = "ciphers.dat") -> None:
    message_bytes_len = len(message.encode('utf-8'))

    with open(filename, "w") as f:
        for _ in range(n):
            key = get_random_bytes(message_bytes_len)
            cipher_hex = encrypt(message, key)
            f.write(cipher_hex + "\n")


flag = "REDACTED"
num_ciphers = 20
#generate_ciphers(flag, num_ciphers)