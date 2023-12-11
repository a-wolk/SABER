import numpy as np
import custom_types as T
from constants import N, Q, P
import math

def BS2POLx(x):
    x = int(math.log2(x))
    def func(bytes: T.Bytes) -> T.Poly:
        out = np.zeros((N,), dtype=np.int64)

        bytes_last = x*N//8-1
        for i in range(N):
            start_byte = bytes_last - (i*x) // 8
            start_offset = (i*x) % 8
            end_byte = bytes_last - ((i+1)*x) // 8
            end_offset = 8 - ((i+1)*x) % 8
            is_3_bytes = (start_byte - end_byte) > 1
            
            out[i] = (bytes[start_byte] & (0xff << start_offset)) >> start_offset
            out[i] |= (bytes[start_byte-1] << (8-start_offset)) if is_3_bytes else 0
            out[i] |= (bytes[end_byte] & (0xff >> end_offset)) << ((8-start_offset) + 8*is_3_bytes)
        return out
    return func

BS2POLp = BS2POLx(2**P)
BS2POLq = BS2POLx(2**Q)

def BS2POL2(bytes: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.int64)

    bytes_last = N//8-1
    for i in range(N):
        start_byte = bytes_last - i // 8
        start_offset = i % 8

        out[i] = (bytes[start_byte] & (0x1 << start_offset)) >> start_offset
    return out

def BS2POLVECx(x):
    bs2pol_x = BS2POLx(x)
    x = int(math.log2(x))
    def func(bytes: T.Bytes) -> T.PolyVector:
        bytes = bytes.reshape((-1, x*N//8))
        l = bytes.shape[0]
        out = np.zeros((l,N), dtype=np.int64)
        for i in range(l):
            out[i, :] = bs2pol_x(bytes[l-i-1, :])
        return out
    return func

BS2POLVECp = BS2POLVECx(2**P)
BS2POLVECq = BS2POLVECx(2**Q)

def POLx2BS(x):
    x = int(math.log2(x))
    def func(p: T.Poly) -> T.Bytes:
        out = np.zeros((x*N//8,), dtype=np.uint8)

        bytes_last = x*N//8-1
        for i in range(N):
            start_byte = bytes_last - (i*x) // 8
            start_offset = (i*x) % 8
            end_byte = bytes_last - ((i+1)*x) // 8
            end_offset = 8 - ((i+1)*x) % 8
            is_3_bytes = (start_byte - end_byte) > 1

            out[start_byte] |= (p[i] & (0xff >> (8-start_offset))) << start_offset
            if is_3_bytes:
                out[start_byte-1] |= (p[i] & (0xff << (8-start_offset))) >> (8-start_offset)
            out[end_byte] |= (p[i] & ((0xff >> end_offset) << ((8-start_offset) + 8*is_3_bytes))) >> ((8-start_offset) + 8*is_3_bytes)
        return out
    return func

POLq2BS = POLx2BS(2**Q)
POLp2BS = POLx2BS(2**P)

def POL22BS(p: T.Poly) -> T.Bytes:
    out = np.zeros((N//8,), dtype=np.uint8)

    bytes_last = N//8-1
    for i in range(N):
        start_byte = bytes_last - i // 8
        start_offset = i % 8

        out[start_byte] |= (p[i] & 0x01) << start_offset
    return out

def POLVECx2BS(x):
    pol_x_2bs = POLx2BS(x)
    x = int(math.log2(x))
    def func(v: T.PolyVector) -> T.Bytes:
        l = v.shape[0]
        out = np.zeros((l*x*N//8,), dtype=np.uint8)
        for i in range(l):
            out[(l-i-1)*x*N//8:(l-i)*x*N//8] = pol_x_2bs(v[i, :])
        return out
    return func

POLVECq2BS = POLVECx2BS(2**Q)
POLVECp2BS = POLVECx2BS(2**P)
