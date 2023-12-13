from keygen import keygen
from encrypt import encrypt
from decrypt import decrypt
from constants import LIGHT_PARAMS, FIRE_PARAMS
import numpy as np
from rng import randombytes

params = LIGHT_PARAMS

(pk, sk) = keygen(params)

m = np.random.randint(0, 256, size=(32,), dtype=np.uint8)
print(m.tolist())

e = encrypt(
    m, 
    randombytes(params.SABER_SEEDBYTES), 
    pk, 
    params
)

d = decrypt(e, sk, params)

print(d.tolist())
print((m == d).all())
