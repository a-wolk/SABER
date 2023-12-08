from keygen import keygen
from encrypt import encrypt
from decrypt import decrypt
from constants import LIGHT_PARAMS
import numpy as np
from rng import randombytes

(pk, sk) = keygen(LIGHT_PARAMS)

m = np.random.randint(0, 256, size=(256,), dtype=np.uint8)
print(m.tolist())

e = encrypt(
    m, 
    randombytes(LIGHT_PARAMS.SABER_SEEDBYTES), 
    pk, 
    LIGHT_PARAMS
)

d = decrypt(e, sk, LIGHT_PARAMS)

print(d.tolist())
print(m == d)