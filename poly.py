import numpy as np
import custom_types as T
from constants import PARAMS, N, Q
from bs2 import BS2POLVECq
from hash import shake128
from cbd import cbd

def gen_matrix(seed: T.Bytes, params: PARAMS) -> T.PolyMatrix:
    buf = shake128(seed, params.SABER_L*params.SABER_L*Q*N//8).reshape((params.SABER_L, params.SABER_L, Q*N//8))
    A = np.zeros((params.SABER_L, params.SABER_L, N), dtype=np.uint16)
    for i in range(params.SABER_L):
        A[i, :, :] = BS2POLVECq(buf[i, :, :], params)
    return A

def hamming(bits: np.uint8):
    return sum(list(map(int, bin(bits)[2:])))

def gen_secret(seed: T.Bytes, params: PARAMS) -> T.PolyVector:
    buf = shake128(seed, params.SABER_L*params.SABER_MU*N//8)
    out = np.zeros((params.SABER_L, N), dtype=np.uint16)

    for i in range(params.SABER_L):
        out[i, :] = cbd(buf[i*params.SABER_MU*N//8:(i+1)*params.SABER_MU*N//8], params.SABER_MU)

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