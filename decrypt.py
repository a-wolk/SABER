import custom_types as T
from poly import shiftright, shiftleft
from constants import PARAMS, P
from poly_mul import inner_prod
from bs2 import BS2POLVECq, BS2POLx, BS2POLVECp, POL22BS

def decrypt(cipher_text: T.Bytes, secret_key: T.Bytes, params: PARAMS) -> T.Bytes:
    s = BS2POLVECq(secret_key)

    cm, ct = cipher_text
    BS2POLt = BS2POLx(2**params.SABER_ET)
    cm = BS2POLt(cm)
    cm = shiftleft(cm, P - params.SABER_ET)

    b = BS2POLVECp(ct)
    v = inner_prod(b, s % (2**P), 2**P, params)

    m = shiftright((v - cm + params.H2) % (2**P), P-1)
    m = POL22BS(m)

    return m