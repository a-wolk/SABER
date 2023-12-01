import numpy as np
import custom_types as T

def randombytes(n: int) -> T.Bytes:
    return np.random.randint(0, 2**8, size=(n,))
