import numpy as np
import custom_types as T
from constants import N, Q, P


def BS2POLx(x):
    def func(bytes: T.Bytes) -> T.Poly:
        out = np.zeros((N,), dtype=np.uint16)

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

BS2POLp = BS2POLx(P)
BS2POL2 = BS2POLx(2)
BS2POLq = BS2POLx(Q)

def BS2POLVECx(x):
    def func(bytes: T.Bytes) -> T.PolyVector:
        bytes = bytes.reshape((-1, x*N//8))
        l = bytes.shape[0]
        out = np.zeros((l,N), dtype=np.uint16)
        bs2pol_x = BS2POLx(x)
        for i in range(l):
            out[i, :] = bs2pol_x(bytes[l-i-1, :])
        return out
    return func

BS2POLVECp = BS2POLVECx(P)
BS2POLVECq = BS2POLVECx(Q)

def POLx2BS(x):
    def func(p: T.Poly) -> T.Bytes:
        out = np.zeros((x*N//8,), dtype=np.uint8)

        bytes_last = x*N//8-1
        for i in range(N):
            start_byte = bytes_last - (i*x) // 8
            start_offset = (i*x) % 8
            end_byte = bytes_last - ((i+1)*x) // 8
            end_offset = 8 - ((i+1)*x) % 8
            is_3_bytes = (start_byte - end_byte) > 1

            out[end_byte] |= ((p[i] & 0xff00) >> (8 + (8 - end_offset)))
            if is_3_bytes:
                out[end_byte+1] |= ((p[i] >> start_offset) & 0xff)
            out[start_byte] |= ((p[i] & (0xff >> start_offset)) << start_offset)
        return out
    return func

POLq2BS = POLx2BS(Q)
POLp2BS = POLx2BS(P)
POL2BS = POLx2BS(2)

def POLVECx2BS(x):
    def func(v: T.PolyVector) -> T.Bytes:
        l = v.shape[0]
        out = np.zeros((l*x*N//8,), dtype=np.uint8)
        pol_x_2bs = POLx2BS(x)
        for i in range(l):
            out[i*x*N//8:(i+1)*x*N//8] = pol_x_2bs(v[i, :])
        return out
    return func

POLVECq2BS = POLVECx2BS(Q)
POLVECp2BS = POLVECx2BS(P)
