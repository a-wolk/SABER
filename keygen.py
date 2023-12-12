import custom_types as T
from typing import Tuple
from constants import PARAMS, Q, P
from rng import randombytes
from hash import shake128
from poly import gen_matrix, gen_secret, shiftright
from poly_mul import matrix_vector_mul
from bs2 import POLVECq2BS, POLVECp2BS

import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

def keygen(params: PARAMS) -> Tuple[Tuple[T.Bytes, T.Bytes], T.Bytes]:
    seed_a = np.array([6,21,80,35,77,21,140,94,201,85,149,254,4,239,122,37,118,127,46,36,204,43,196,121,208,157,134,220,154,188,253,231], dtype=np.uint8) #randombytes(params.SABER_SEEDBYTES)
    seed_a = shake128(seed_a, params.SABER_SEEDBYTES)
    seed_s = np.array([26,159,188,188,141,163,109,255,42,190,32,50,150,23,15,219,151,195,41,127,103,252,182,121,172,113,156,159,208,2,83,176], dtype=np.uint8) #randombytes(params.SABER_NOISE_SEEDBYTES)

    A = gen_matrix(seed_a, params)
    s = gen_secret(seed_s, params)
    b = matrix_vector_mul(A, s, True, 2**Q, params)
    b += params.H
    b %= (2**Q)

    for i in range(params.SABER_L):
        b[i, :] = shiftright(b[i, :], Q-P)

    secret_key = POLVECq2BS(s)
    pk = POLVECp2BS(b)

    return ((seed_a, pk), secret_key)
