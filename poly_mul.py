import numpy as np
import custom_types as T
from constants import PARAMS, N
from numpy.polynomial import polynomial as poly

def poly_mul(a: T.Poly, b: T.Poly, q: int, params: PARAMS) -> T.Poly:
    # TODO
    # TODO
    # TODO
    c = params.POLYNOMIAL_COEFF
    a_mul_b = (poly.polymul(a.astype(np.uint64), b.astype(np.uint64)).astype(np.uint64) % q).astype(np.uint16)
    a_mul_b = np.pad(a_mul_b, (2*N-len(a_mul_b), 0), 'constant', constant_values=(0, 0))
    return (a_mul_b[:N] - a_mul_b[N:])
    # a_mul_b_mod_c = np.polydiv(a_mul_b, c)[1].astype(np.uint16) 
    # out = a_mul_b_mod_c
    # return np.pad(out, (N-len(out),0), 'constant', constant_values=(0, 0))

def matrix_vector_mul(A: T.PolyMatrix, v: T.PolyVector, transpose: bool, q: int, params: PARAMS) -> T.PolyVector:
    out = np.zeros(params.POLYVEC_SHAPE, dtype=np.uint16)
    for i in range(params.SABER_L):
        c = np.zeros(params.POLY_SHAPE, dtype=np.uint16)
        for j in range(params.SABER_L):
            if transpose:
                c += poly_mul(A[j, i, :], v[j, :], q, params)
            else:
                c += poly_mul(A[i, j, :], v[j, :], q, params)
        out[i, :] = c
    return out

def inner_prod(a: T.PolyVector, b: T.PolyVector, q: int, params: PARAMS) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    for i in range(params.SABER_L):
        out += poly_mul(a[i, :], b[i, :], q, params)
    return out % q