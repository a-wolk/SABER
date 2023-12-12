import numpy as np
import custom_types as T

def randombytes(n: int) -> T.Bytes:
    return np.random.randint(0, 2**8, size=(n,))
# RANDOM_BYTES_HARDCODED = True

# def randombytes(n: int) -> T.Bytes:
#     if RANDOM_BYTES_HARDCODED:
#         return np.ones(size=(n,))
#     else:
#         return np.random.randint(0, 2**8, size=(n,))
