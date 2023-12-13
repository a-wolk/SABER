import custom_types as T
from poly import gen_matrix, gen_secret, shiftright, shiftleft
from constants import PARAMS, Q, P
from poly_mul import matrix_vector_mul, inner_prod
from bs2 import BS2POLVECp, BS2POL2, POLT2BS, POLVECp2BS

def encrypt(m: T.Bytes, seed_s: T.Bytes, pk: T.PublicKey, params: PARAMS) -> T.Bytes:
    seed_a, pk = pk

    A = gen_matrix(seed_a, params)
    s = gen_secret(seed_s, params)
    bp = (matrix_vector_mul(A, s, False, params) + params.H) % (2**Q)

    for i in range(params.SABER_L):
        bp[i, :] = shiftright(bp[i, :], Q-P)

    b = BS2POLVECp(pk, params)
    v = inner_prod(b, s % (2**P), params)

    mp = BS2POL2(m)
    mp = shiftleft(mp, P-1)
    cm = shiftright((v - mp + params.H1) % (2**P), P - params.SABER_ET)

    return (POLT2BS(cm, params.SABER_ET), POLVECp2BS(bp, params))
