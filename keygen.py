import custom_types as T
from typing import Tuple
from constants import PARAMS, Q, P
from rng import randombytes
from hash import shake128
from poly import gen_matrix, gen_secret, shiftright
from poly_mul import matrix_vector_mul
from bs2 import POLVECq2BS, POLVECp2BS

def keygen(params: PARAMS) -> Tuple[Tuple[T.Bytes, T.Bytes], T.Bytes]:
    seed_a = randombytes(params.SABER_SEEDBYTES)
    seed_a = shake128(seed_a, params.SABER_SEEDBYTES)
    seed_s = randombytes(params.SABER_NOISE_SEEDBYTES)

    A = gen_matrix(seed_a, params)
    s = gen_secret(seed_s, params)

    b = matrix_vector_mul(A, s, True, params)

    h1 = (1 << (Q - P - 1))
    for i in range(params.SABER_L):
        b[i, :] = shiftright(b[i, :] + h1, Q-P)

    secret_key = POLVECq2BS(s, params)
    pk = POLVECp2BS(b, params)

    return ((seed_a, pk), secret_key)
