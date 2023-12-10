import numpy as np
import custom_types as T
from constants import PARAMS, N

def poly_mul(a: T.Poly, b: T.Poly, q: int, params: PARAMS) -> T.Poly:
    return np.polynomial.polynomial.polydiv(np.polynomial.polynomial.polymul(a, b), params.POLYNOMIAL_COEFF)[1].astype(np.uint16) % q

def matrix_vector_mul(A: T.PolyMatrix, v: T.PolyVector, q: int, transpose: bool, params: PARAMS) -> T.PolyVector:
    out = np.zeros(params.POLYVEC_SHAPE, dtype=np.uint16)
    for i in range(params.SABER_L):
        c = np.zeros(params.POLY_SHAPE, dtype=np.uint16)
        for j in range(params.SABER_L):
            if transpose:
                c += poly_mul(A[j, i, :], v[j, :], q, params)
            else:
                c += poly_mul(A[i, j, :], v[j, :], q, params)
        out[i, :] = c % q
    return out

def inner_prod(a: T.PolyVector, b: T.PolyVector, q: int, params: PARAMS) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    for i in range(params.SABER_L):
        out += poly_mul(a[i, :], b[i, :], q, params)
    return out % q