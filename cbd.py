import numpy as np
import custom_types as T
from constants import PARAMS, N

def load_littleendian(x, n_bytes):
    r = x[0]
    for i in range(1, n_bytes):
        r |= int(x[i]) << (8 * i)
    return r

def cbd(buf: T.Bytes, mu: int) -> T.Poly:
    if mu == 6:
        return cbd6(buf)
    elif mu == 8:
        return cbd8(buf)
    elif mu == 10:
        return cbd10(buf)

def cbd10(buf: T.Bytes) -> T.Poly:
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

def cbd6(buf: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    
    t = 0
    d = 0
    a = [0, 0, 0, 0]
    b = [0, 0, 0, 0]
    for i in range(N // 4):
        t = load_littleendian(buf + 3 * i, 3)
        d = 0
        for j in range(3):
            d += (t >> j) & 0x249249

        a[0] = d & 0x7
        b[0] = (d >> 3) & 0x7
        a[1] = (d >> 6) & 0x7
        b[1] = (d >> 9) & 0x7
        a[2] = (d >> 12) & 0x7
        b[2] = (d >> 15) & 0x7
        a[3] = (d >> 18) & 0x7
        b[3] = (d >> 21)

        out[4 * i + 0] = a[0] - b[0]
        out[4 * i + 1] = a[1] - b[1]
        out[4 * i + 2] = a[2] - b[2]
        out[4 * i + 3] = a[3] - b[3]
    return out

def cbd8(buf: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    
    t = 0
    d = 0
    a = [0, 0, 0, 0]
    b = [0, 0, 0, 0]
    for i in range(N // 4):
        t = load_littleendian(buf + 4 * i, 4)
        d = 0
        for j in range(4):
            d += (t >> j) & 0x11111111

        a[0] = d & 0xf
        b[0] = (d >> 4) & 0xf
        a[1] = (d >> 8) & 0xf
        b[1] = (d >> 12) & 0xf
        a[2] = (d >> 16) & 0xf
        b[2] = (d >> 20) & 0xf
        a[3] = (d >> 24) & 0xf
        b[3] = (d >> 28)

        out[4 * i + 0] = a[0] - b[0]
        out[4 * i + 1] = a[1] - b[1]
        out[4 * i + 2] = a[2] - b[2]
        out[4 * i + 3] = a[3] - b[3]
    return out