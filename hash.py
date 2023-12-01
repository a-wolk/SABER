import hashlib
import numpy as np
import custom_types as T

def shake128(_bytes: T.Bytes, n: int) -> T.Bytes:
    _bytes = bytes(_bytes.tolist())
    _bytes = hashlib.shake_128(_bytes).digest(n)
    return np.array(list(_bytes), dtype=np.uint8)
