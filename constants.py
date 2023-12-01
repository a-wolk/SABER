import numpy as np

N = 256
Q = 13
P = 10

class PARAMS():
    def __init__(
            self,
            SABER_L,
            SABER_EQ,
            SABER_EP,
            SABER_MU,
            SABER_ET,
            SABER_SEEDBYTES,
            SABER_NOISE_SEEDBYTES,
            SABER_KEYBYTES,
            SABER_HASHBYTES,
            SABER_INDCPA_PUBLICKEYBYTES,
            SABER_INDCPA_SECRETKEYBYTES,
            SABER_PUBLICKEYBYTES,
            SABER_SECRETKEYBYTES,
            SABER_BYTES_CCA_DEC
        ) -> None:
        self.SABER_L = SABER_L
        self.SABER_EQ = SABER_EQ
        self.SABER_EP = SABER_EP
        self.SABER_MU = SABER_MU
        self.SABER_ET = SABER_ET
        self.SABER_SEEDBYTES = SABER_SEEDBYTES
        self.SABER_NOISE_SEEDBYTES = SABER_NOISE_SEEDBYTES
        self.SABER_KEYBYTES = SABER_KEYBYTES
        self.SABER_HASHBYTES = SABER_HASHBYTES
        self.SABER_INDCPA_PUBLICKEYBYTES = SABER_INDCPA_PUBLICKEYBYTES
        self.SABER_INDCPA_SECRETKEYBYTES = SABER_INDCPA_SECRETKEYBYTES
        self.SABER_PUBLICKEYBYTES = SABER_PUBLICKEYBYTES
        self.SABER_SECRETKEYBYTES = SABER_SECRETKEYBYTES
        self.SABER_BYTES_CCA_DEC = SABER_BYTES_CCA_DEC
        self.POLY_SHAPE = (N,)
        self.POLYVEC_SHAPE = (SABER_L, N)
        self.POLYMATRIX_SHAPE = (SABER_L, SABER_L, N)
        self.POLYNOMIAL_COEFF = np.zeros((N+1,), dtype=np.uint16)
        self.POLYNOMIAL_COEFF[0] = 1
        self.POLYNOMIAL_COEFF[-1] = 1

LIGHT_PARAMS = PARAMS(
    SABER_L = 2,
    SABER_EQ = 13,
    SABER_EP = 10,
    SABER_MU = 10,
    SABER_ET = 3,
    SABER_SEEDBYTES = 32,
    SABER_NOISE_SEEDBYTES = 32,
    SABER_KEYBYTES = 32,
    SABER_HASHBYTES = 32,
    SABER_INDCPA_PUBLICKEYBYTES = 672,
    SABER_INDCPA_SECRETKEYBYTES = 832,
    SABER_PUBLICKEYBYTES = 672,
    SABER_SECRETKEYBYTES = 1568,
    SABER_BYTES_CCA_DEC = 736
)

SABER_PARAMS = PARAMS(
    SABER_L = 3,
    SABER_EQ = 13,
    SABER_EP = 10,
    SABER_MU = 8,
    SABER_ET = 4,
    SABER_SEEDBYTES = 32,
    SABER_NOISE_SEEDBYTES = 32,
    SABER_KEYBYTES = 32,
    SABER_HASHBYTES = 32,
    SABER_INDCPA_PUBLICKEYBYTES = 992,
    SABER_INDCPA_SECRETKEYBYTES = 1248,
    SABER_PUBLICKEYBYTES = 992,
    SABER_SECRETKEYBYTES = 2304,
    SABER_BYTES_CCA_DEC = 1088
)

FIRE_PARAMS = PARAMS(
    SABER_L = 4,
    SABER_EQ = 13,
    SABER_EP = 10,
    SABER_MU = 6,
    SABER_ET = 6,
    SABER_SEEDBYTES = 32,
    SABER_NOISE_SEEDBYTES = 32,
    SABER_KEYBYTES = 32,
    SABER_HASHBYTES = 32,
    SABER_INDCPA_PUBLICKEYBYTES = 1312,
    SABER_INDCPA_SECRETKEYBYTES = 1664,
    SABER_PUBLICKEYBYTES = 1312,
    SABER_SECRETKEYBYTES = 3040,
    SABER_BYTES_CCA_DEC = 1472
)