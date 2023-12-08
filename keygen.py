import custom_types as T
from typing import Tuple
from constants import PARAMS, Q, P, LIGHT_PARAMS
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
    b = (matrix_vector_mul(A, s, 2**Q, True, params) + params.H) % (2**Q)

    for i in range(params.SABER_L):
        b[i, :] = shiftright(b[i, :], Q-P)

    secret_key = POLVECq2BS(s)
    pk = POLVECp2BS(b)

    return ((seed_a, pk), secret_key)

print(keygen(LIGHT_PARAMS))