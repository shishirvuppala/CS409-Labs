# Faulty PRG
# Seed: upto 32 bytes (256 bits)
# State: 256 bits
import os
A = 6364136223846793005
C = 1442695040888963407
M = 2**256

def prg(seed):
    if len(seed) > 32:
        raise ValueError("Seed must be at most 32 bytes")

    state = int.from_bytes(seed, "big")

    for _ in range(5):
        state = (A * state + C) % M

        yield state >> 8

flag = b"REDACTED"

generator = prg(flag)

with open("output.txt", "w") as f:
    for output in generator:
        f.write(f"{output:062x}")
