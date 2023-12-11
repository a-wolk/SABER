import numpy as np
import custom_types as T
from constants import PARAMS, N, Q
from bs2 import BS2POLVECq
from hash import shake128

def gen_matrix(seed: T.Bytes, params: PARAMS) -> T.PolyMatrix:
    buf = shake128(seed, params.SABER_L*params.SABER_L*Q*N//8).reshape((params.SABER_L, params.SABER_L, Q*N//8))
    A = np.zeros((params.SABER_L, params.SABER_L, N), dtype=np.int64)
    for i in range(params.SABER_L):
        A[i, :, :] = BS2POLVECq(buf[params.SABER_L-i-1, :, :])
    return A

def hamming(bits: np.uint8):
    return sum(list(map(int, bin(bits)[2:])))

def gen_secret(seed: T.Bytes, params: PARAMS) -> T.PolyVector:
    buf = shake128(seed, params.SABER_L*params.SABER_MU*N//8)
    out = np.zeros((params.SABER_L, N), dtype=np.int64)

    last_byte = params.SABER_L*params.SABER_MU*N//8 - 1
    for i in range(params.SABER_L):
        for j in range(N):
            start_byte = last_byte - ((i*N + j)*params.SABER_MU // 8)
            start_offset = (i*N + j)*params.SABER_MU % 8
            end_byte = last_byte - ((i*N + j + 1)*params.SABER_MU // 8)
            end_offset = 8 - ((i*N + j + 1)*params.SABER_MU % 8)
            is_3_bytes = (start_byte - end_byte) > 1

            value = 0
            value = (buf[start_byte] & (0xff << start_offset)) >> start_offset
            if is_3_bytes:
                value |= (buf[start_byte-1] << (8-start_offset))
            value |= (buf[end_byte] & (0xff >> end_offset)) << ((8-start_offset) + 8*int(is_3_bytes))

            mask = (0xffff << (params.SABER_MU//2))
            out[i, j] = (hamming(value & (~mask)) - hamming(value & mask)) % 2**Q
    return out

def shiftright(pol: T.Poly, s: int) -> T.Poly:
    out = pol.copy()
    for i in range(N):
        out[i] >>= s
    return out

def shiftleft(pol: T.Poly, s: int) -> T.Poly:
    out = pol.copy()
    for i in range(N):
        out[i] <<= s
    return out

#print(gen_matrix(randombytes(LIGHT_PARAMS.SABER_SEEDBYTES), LIGHT_PARAMS).tolist())
#print(gen_secret(randombytes(LIGHT_PARAMS.SABER_NOISE_SEEDBYTES), LIGHT_PARAMS).tolist())