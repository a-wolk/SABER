import numpy as np
import custom_types as T
from constants import PARAMS, N

SCHB_N = 16

N_RES = (N << 1)
N_SB = (N >> 2)
N_SB_RES = (2*N_SB-1)

KARATSUBA_N = 64
def karatsuba_simple(a_1, b_1):
    out = np.zeros((N_SB_RES,), dtype=np.uint16)

    d01 = np.zeros((KARATSUBA_N // 2 - 1,), dtype=np.uint16)
    d0123 = np.zeros((KARATSUBA_N // 2 - 1,), dtype=np.uint16)
    d23 = np.zeros((KARATSUBA_N // 2 - 1,), dtype=np.uint16)
    result_d01 = np.zeros((KARATSUBA_N - 1,), dtype=np.uint16)

    acc1 = 0
    acc2 = 0
    acc3 = 0
    acc4 = 0
    acc5 = 0
    acc6 = 0
    acc7 = 0
    acc8 = 0
    acc9 = 0
    acc10 = 0

    for i in range(KARATSUBA_N // 4):
        acc1 = a_1[i]
        acc2 = a_1[i + KARATSUBA_N // 4]
        acc3 = a_1[i + 2 * KARATSUBA_N // 4]
        acc4 = a_1[i + 3 * KARATSUBA_N // 4]
        for j in range(KARATSUBA_N // 4):
            acc5 = b_1[j]
            acc6 = b_1[j + KARATSUBA_N // 4]

            out[i + j + 0 * KARATSUBA_N // 4] += np.array(acc1 * acc5).astype(np.uint16) #OVERFLOW
            out[i + j + 2 * KARATSUBA_N // 4] += np.array(acc2 * acc6).astype(np.uint16) #OVERFLOW

            acc7 = acc5 + acc6
            acc8 = acc1 + acc2
            d01[i + j] = d01[i + j] + np.array(acc7 * acc8).astype(np.uint16)

            acc7 = b_1[j + 2 * KARATSUBA_N // 4]
            acc8 = b_1[j + 3 * KARATSUBA_N // 4]
            out[i + j + 4 * KARATSUBA_N // 4] += np.array(acc7 * acc3).astype(np.uint16) #OVERFLOW
            out[i + j + 6 * KARATSUBA_N // 4] += np.array(acc8 * acc4).astype(np.uint16) #OVERFLOW

            acc9 = acc3 + acc4
            acc10 = acc7 + acc8
            d23[i + j] = d23[i + j] + np.array(acc9 * acc10).astype(np.uint16) #OVERFLOW

            acc5 = acc5 + acc7
            acc7 = acc1 + acc3
            result_d01[i + j + 0 * KARATSUBA_N // 4] += np.array(acc5 * acc7).astype(np.uint16) #OVERFLOW

            acc6 = acc6 + acc8
            acc8 = acc2 + acc4
            result_d01[i + j + 2 * KARATSUBA_N // 4] += np.array(acc6 * acc8).astype(np.uint16) #OVERFLOW

            acc5 = acc5 + acc6
            acc7 = acc7 + acc8
            d0123[i + j] = d0123[i + j] + np.array(acc5 * acc7).astype(np.uint16) #OVERFLOW

    for i in range(KARATSUBA_N // 2 - 1):
        d0123[i] = d0123[i] - result_d01[i + 0 * KARATSUBA_N // 4] - result_d01[i + 2 * KARATSUBA_N // 4]
        d01[i] = d01[i] - out[i + 0 * KARATSUBA_N // 4] - out[i + 2 * KARATSUBA_N // 4]
        d23[i] = d23[i] - out[i + 4 * KARATSUBA_N // 4] - out[i + 6 * KARATSUBA_N // 4]

    for i in range(KARATSUBA_N // 2 - 1):
        result_d01[i + 1 * KARATSUBA_N // 4] = result_d01[i + 1 * KARATSUBA_N // 4] + d0123[i]
        out[i + 1 * KARATSUBA_N // 4] = out[i + 1 * KARATSUBA_N // 4] + d01[i]
        out[i + 5 * KARATSUBA_N // 4] = out[i + 5 * KARATSUBA_N // 4] + d23[i]

    for i in range(KARATSUBA_N - 1):
        result_d01[i] = result_d01[i] - out[i] - out[i + KARATSUBA_N]

    for i in range(KARATSUBA_N - 1):
        out[i + 1 * KARATSUBA_N // 2] = out[i + 1 * KARATSUBA_N // 2] + result_d01[i]

    return out



def toom_cook_4way(a1, b1):
    result = np.zeros((2*N), dtype=np.uint16)
    inv3 = 43691
    inv9 = 36409
    inv15 = 61167

    aw1 = np.zeros((N_SB,), dtype=np.uint16)
    aw2 = np.zeros((N_SB,), dtype=np.uint16)
    aw3 = np.zeros((N_SB,), dtype=np.uint16)
    aw4 = np.zeros((N_SB,), dtype=np.uint16)
    aw5 = np.zeros((N_SB,), dtype=np.uint16)
    aw6 = np.zeros((N_SB,), dtype=np.uint16)
    aw7 = np.zeros((N_SB,), dtype=np.uint16)

    bw1 = np.zeros((N_SB,), dtype=np.uint16)
    bw2 = np.zeros((N_SB,), dtype=np.uint16)
    bw3 = np.zeros((N_SB,), dtype=np.uint16)
    bw4 = np.zeros((N_SB,), dtype=np.uint16)
    bw5 = np.zeros((N_SB,), dtype=np.uint16)
    bw6 = np.zeros((N_SB,), dtype=np.uint16)
    bw7 = np.zeros((N_SB,), dtype=np.uint16)

    w1 = np.zeros((N_SB_RES,), dtype=np.uint16)
    w2 = np.zeros((N_SB_RES,), dtype=np.uint16)
    w3 = np.zeros((N_SB_RES,), dtype=np.uint16)
    w4 = np.zeros((N_SB_RES,), dtype=np.uint16)
    w5 = np.zeros((N_SB_RES,), dtype=np.uint16)
    w6 = np.zeros((N_SB_RES,), dtype=np.uint16)
    w7 = np.zeros((N_SB_RES,), dtype=np.uint16)

    r0 = 0
    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0
    r5 = 0
    r6 = 0
    r7 = 0

    for j in range(N_SB):
        r0 = a1[j]
        r1 = a1[N_SB + j]
        r2 = a1[2*N_SB + j]
        r3 = a1[3*N_SB + j]
        r4 = r0 + r2
        r5 = r1 + r3
        r6 = r4 + r5
        r7 = r4 - r5
        aw3[j] = r6
        aw4[j] = r7
        r4 = ((r0 << 2) + r2) << 1
        r5 = (r1 << 2) + r3
        r6 = r4 + r5
        r7 = r4 - r5
        aw5[j] = r6
        aw6[j] = r7
        r4 = (r3 << 3) + (r2 << 2) + (r1 << 1) + r0
        aw2[j] = r4
        aw7[j] = r0
        aw1[j] = r3
    
    for j in range(N_SB):
        r0 = b1[j]
        r1 = b1[N_SB + j]
        r2 = b1[2*N_SB + j]
        r3 = b1[3*N_SB + j]
        r4 = r0 + r2
        r5 = r1 + r3
        r6 = r4 + r5
        r7 = r4 - r5
        bw3[j] = r6
        bw4[j] = r7
        r4 = ((r0 << 2) + r2) << 1
        r5 = (r1 << 2) + r3
        r6 = r4 + r5
        r7 = r4 - r5
        bw5[j] = r6
        bw6[j] = r7
        r4 = (r3 << 3) + (r2 << 2) + (r1 << 1) + r0
        bw2[j] = r4
        bw7[j] = r0
        bw1[j] = r3

    w1 = karatsuba_simple(aw1, bw1)
    w2 = karatsuba_simple(aw2, bw2)
    w3 = karatsuba_simple(aw3, bw3)
    w4 = karatsuba_simple(aw4, bw4)
    w5 = karatsuba_simple(aw5, bw5)
    w6 = karatsuba_simple(aw6, bw6)
    w7 = karatsuba_simple(aw7, bw7)

    for i in range(N_SB_RES):
        r0 = w1[i]
        r1 = w2[i]
        r2 = w3[i]
        r3 = w4[i]
        r4 = w5[i]
        r5 = w6[i]
        r6 = w7[i]

        r1 = r1 + r4
        r5 = r5 - r4
        r3 = ((r3 - r2) >> 1)
        r4 = r4 - r0
        r4 = r4 - (r6 << 6)
        r4 = (r4 << 1) + r5
        r2 = r2 + r3
        r1 = r1 - (r2 << 6) - r2
        r2 = r2 - r6
        r2 = r2 - r0
        r1 = r1 + 45 * r2
        r4 = np.array(((r4 - (r2 << 3)) * inv3) >> 3).astype(np.uint16)
        r5 = r5 + r1
        r1 = np.array(((r1 + (r3 << 4)) * inv9) >> 1).astype(np.uint16)
        r3 = -(r3 + r1)
        r5 = np.array(((30 * r1 - r5) * inv15) >> 2).astype(np.uint16)
        r2 = r2 - r4
        r1 = r1 - r5

        result[i]     += r6
        result[i + 64]  += r5
        result[i + 128] += r4
        result[i + 192] += r3
        result[i + 256] += r2
        result[i + 320] += r1
        result[i + 384] += r0
    return result

def poly_mul(a: T.Poly, b: T.Poly) -> T.Poly:
    result = toom_cook_4way(a, b)
    return result[:N] - result[N:]

def matrix_vector_mul(A: T.PolyMatrix, v: T.PolyVector, transpose: bool, params: PARAMS) -> T.PolyVector:
    out = np.zeros(params.POLYVEC_SHAPE, dtype=np.uint16)
    for i in range(params.SABER_L):
        c = np.zeros(params.POLY_SHAPE, dtype=np.uint16)
        for j in range(params.SABER_L):
            if transpose:
                c += poly_mul(A[j, i, :], v[j, :])
            else:
                c += poly_mul(A[i, j, :], v[j, :])
        out[i, :] = c
    return out

def inner_prod(a: T.PolyVector, b: T.PolyVector, params: PARAMS) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    for i in range(params.SABER_L):
        out += poly_mul(a[i, :], b[i, :])
    return out
