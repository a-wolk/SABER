import numpy as np
import custom_types as T
from constants import PARAMS, N

def load_littleendian(x, n_bytes):
    r = x[0]
    for i in range(1, n_bytes):
        r |= int(x[i]) << (8 * i)
    return r

def cbd(buf: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    
    t = 0
    d = 0
    a = [0, 0, 0, 0]
    b = [0, 0, 0, 0]
    for i in range(N // 4):
        t = load_littleendian(buf[5 * i:], 5)
        d = 0
        for j in range(5):
            d += (t >> j) & 0x0842108421

            a[0] = d & 0x1f
            b[0] = (d >> 5) & 0x1f
            a[1] = (d >> 10) & 0x1f
            b[1] = (d >> 15) & 0x1f
            a[2] = (d >> 20) & 0x1f
            b[2] = (d >> 25) & 0x1f
            a[3] = (d >> 30) & 0x1f
            b[3] = (d >> 35)

            out[4 * i + 0] = a[0] - b[0]
            out[4 * i + 1] = a[1] - b[1]
            out[4 * i + 2] = a[2] - b[2]
            out[4 * i + 3] = a[3] - b[3]
    return out
