import custom_types as T
from poly import shiftright, shiftleft
from constants import PARAMS, P
from poly_mul import inner_prod
from bs2 import BS2POLVECq, BS2POLT, BS2POLVECp, POL22BS

def decrypt(cipher_text: T.Bytes, secret_key: T.Bytes, params: PARAMS) -> T.Bytes:
    s = BS2POLVECq(secret_key, params)

    cm, ct = cipher_text
    cm = BS2POLT(cm, params.SABER_ET)
    cm = shiftleft(cm, P - params.SABER_ET)

    b = BS2POLVECp(ct, params)
    v = inner_prod(b, s % (2**P), params)

    m = shiftright((v - cm + params.H2) % (2**P), P-1)
    m = POL22BS(m)

    return m