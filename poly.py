import numpy as np
import numpy.typing as npt
import custom_types as T
from constants import PARAMS, N, Q
from bs2 import BS2OLVECq
from hash import shake128

def gen_matrix(seed: npt.NDArray[np.uint8], params: PARAMS) -> npt.NDArray[np.uint16]:
    buf = shake128(seed, params.SABER_L*params.SABER_L*Q*N//8).reshape((params.SABER_L, params.SABER_L, Q*N//8))
    A = np.zeros((params.SABER_L, params.SABER_L, N), dtype=np.uint16)
    for i in range(params.SABER_L):
        A[i, :, :] = BS2OLVECq(buf[params.SABER_L-i-1, :, :])
    return A

def hamming(bits: np.uint8):
    return (bits & 0x1) + (bits & 0x2) + (bits & 0x4) + (bits & 0x8) + (bits & 0x10) + (bits & 0x20) + (bits & 0x40) + (bits & 0x80)

def gen_secret(seed: npt.NDArray[np.uint8], params: PARAMS) -> npt.NDArray[np.uint16]:
    buf = shake128(seed, params.SABER_L*params.SABER_MU*N//8)
    out = np.zeros((params.SABER_L, N), dtype=np.uint16)

    last_byte = params.SABER_L*params.SABER_MU*N//8 - 1
    for i in range(params.SABER_L):
        for j in range(N):
            start_byte = last_byte - ((i*N + j)*params.SABER_MU // 8)
            start_offset = (i*N + j)*params.SABER_MU % 8
            end_byte = last_byte - ((i*N + j + 1)*params.SABER_MU // 8)
            end_offset = 8 - ((i*N + j + 1)*params.SABER_MU % 8)
            is_3_bytes = (start_byte - end_byte) > 1

            value = 0
            value |= (buf[end_byte] & (0xff >> end_offset)) << ((8 - end_offset) + (8 if is_3_bytes else 0))
            value |= buf[end_byte+1] if is_3_bytes else 0
            value |= (buf[start_byte] >> start_offset)

            out[i, j] = (hamming(value & 0xff) - hamming((value & 0xff00) >> 4)) % 2**Q
    return out

def shiftright(pol: T.Poly, s: int) -> T.Poly:
    out = pol.copy()
    for i in range(N):
        out[i] >>= s
    return out

#print(gen_matrix(randombytes(LIGHT_PARAMS.SABER_SEEDBYTES), LIGHT_PARAMS).tolist())
#print(gen_secret(randombytes(LIGHT_PARAMS.SABER_NOISE_SEEDBYTES), LIGHT_PARAMS).tolist())