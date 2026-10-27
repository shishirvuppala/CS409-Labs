

A = 6364136223846793005
C = 1442695040888963407
M = 2**256

with open("output.txt", "r") as f:
    first_chunk = f.read(62)
num = int(first_chunk, 16)

A_inv = pow(A, -1, M)

for i in range(256):

    state = (num << 8) + i

    prev_state = ((state - C) * A_inv) % M

    try:
        possible_flag = prev_state.to_bytes(32, "big").strip(b'\x00')
        
        if b"cs409{" in possible_flag:
            print(f"FLAG: {possible_flag.decode()}")
            break
    except:
        pass


