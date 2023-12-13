import numpy as np
import custom_types as T
from constants import N, Q, P, PARAMS

def POL3T2BS(p: T.Poly):
    out = np.zeros((3*N//8,), dtype=np.uint8)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 8):
        offset_byte = 3 * j
        offset_data = 8 * j
        out[offset_byte + 0] = (p[offset_data + 0] & 0x7) | ((p[offset_data + 1] & 0x7) << 3) | ((p[offset_data + 2] & 0x3) << 6)
        out[offset_byte + 1] = ((p[offset_data + 2] >> 2) & 0x01) | ((p[offset_data + 3] & 0x7) << 1) | ((p[offset_data + 4] & 0x7) << 4) | (((p[offset_data + 5]) & 0x01) << 7)
        out[offset_byte + 2] = ((p[offset_data + 5] >> 1) & 0x03) | ((p[offset_data + 6] & 0x7) << 2) | ((p[offset_data + 7] & 0x7) << 5)
    return out

def POL4T2BS(p: T.Poly):
    out = np.zeros((4*N//8,), dtype=np.uint8)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 2):
        offset_byte = j
        offset_data = 2 * j
        out[offset_byte] = (p[offset_data] & 0x0f) | ((p[offset_data + 1] & 0x0f) << 4)
    return out

def POL6T2BS(p: T.Poly):
    out = np.zeros((6*N//8,), dtype=np.uint8)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 4):
        offset_byte = 3 * j
        offset_data = 4 * j
        out[offset_byte + 0] = (p[offset_data + 0] & 0x3f) | ((p[offset_data + 1] & 0x03) << 6) 
        out[offset_byte + 1] = ((p[offset_data + 1] >> 2) & 0x0f) | ((p[offset_data + 2] & 0x0f) << 4)
        out[offset_byte + 2] = ((p[offset_data + 2] >> 4) & 0x03) | ((p[offset_data + 3] & 0x3f) << 2)
    return out

def POLT2BS(p: T.Poly, t: int):
    if t == 3:
        return POL3T2BS(p)
    elif t == 4:
        return POL4T2BS(p)
    elif t == 6:
        return POL6T2BS(p)
    
def BS2POL3T(bytes: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 8):
        offset_byte = 3 * j
        offset_data = 8 * j
        out[offset_data + 0] = (bytes[offset_byte + 0]) & 0x07
        out[offset_data + 1] = ((bytes[offset_byte + 0]) >> 3) & 0x07
        out[offset_data + 2] = (((bytes[offset_byte + 0]) >> 6) & 0x03) | (((bytes[offset_byte + 1]) & 0x01) << 2)
        out[offset_data + 3] = ((bytes[offset_byte + 1]) >> 1) & 0x07
        out[offset_data + 4] = ((bytes[offset_byte + 1]) >> 4) & 0x07
        out[offset_data + 5] = (((bytes[offset_byte + 1]) >> 7) & 0x01) | (((bytes[offset_byte + 2]) & 0x03) << 1)
        out[offset_data + 6] = ((bytes[offset_byte + 2] >> 2) & 0x07)
        out[offset_data + 7] = ((bytes[offset_byte + 2] >> 5) & 0x07)
    return out

def BS2POL4T(bytes: T.Bytes):
    out = np.zeros((N,), dtype=np.uint16)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 2):
        offset_byte = j
        offset_data = 2 * j
        out[offset_data] = bytes[offset_byte] & 0x0f
        out[offset_data + 1] = (bytes[offset_byte] >> 4) & 0x0f
    return out

def BS2POL6T(bytes: T.Bytes):
    out = np.zeros((N,), dtype=np.uint16)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 4):
        offset_byte = 3 * j
        offset_data = 4 * j
        out[offset_data + 0] = bytes[offset_byte + 0] & 0x3f
        out[offset_data + 1] = ((bytes[offset_byte + 0] >> 6) & 0x03) | ((bytes[offset_byte + 1] & 0x0f) << 2)
        out[offset_data + 2] = ((bytes[offset_byte + 1] & 0xff) >> 4) | ((bytes[offset_byte + 2] & 0x03) << 4)
        out[offset_data + 3] = ((bytes[offset_byte + 2] & 0xff) >> 2)
    return out

def BS2POLT(bytes: T.Bytes, t: int):
    if t == 3:
        return BS2POL3T(bytes)
    elif t == 4:
        return BS2POL4T(bytes)
    elif t == 6:
        return BS2POL6T(bytes)

def BS2POLp(bytes: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 4):
        offset_byte = 5 * j
        offset_data = 4 * j
        out[offset_data + 0] = (bytes[offset_byte + 0] & (0xff)) | ((bytes[offset_byte + 1] & 0x03) << 8)
        out[offset_data + 1] = ((bytes[offset_byte + 1] >> 2) & (0x3f)) | ((bytes[offset_byte + 2] & 0x0f) << 6)
        out[offset_data + 2] = ((bytes[offset_byte + 2] >> 4) & (0x0f)) | ((bytes[offset_byte + 3] & 0x3f) << 4)
        out[offset_data + 3] = ((bytes[offset_byte + 3] >> 6) & (0x03)) | ((bytes[offset_byte + 4] & 0xff) << 2)
    return out

def BS2POLq(bytes: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 8):
        offset_byte = 13 * j
        offset_data = 8 * j
        out[offset_data + 0] = (bytes[offset_byte + 0] & (0xff)) | ((bytes[offset_byte + 1] & 0x1f) << 8)
        out[offset_data + 1] = (bytes[offset_byte + 1] >> 5 & (0x07)) | ((bytes[offset_byte + 2] & 0xff) << 3) | ((bytes[offset_byte + 3] & 0x03) << 11)
        out[offset_data + 2] = (bytes[offset_byte + 3] >> 2 & (0x3f)) | ((bytes[offset_byte + 4] & 0x7f) << 6)
        out[offset_data + 3] = (bytes[offset_byte + 4] >> 7 & (0x01)) | ((bytes[offset_byte + 5] & 0xff) << 1) | ((bytes[offset_byte + 6] & 0x0f) << 9)
        out[offset_data + 4] = (bytes[offset_byte + 6] >> 4 & (0x0f)) | ((bytes[offset_byte + 7] & 0xff) << 4) | ((bytes[offset_byte + 8] & 0x01) << 12)
        out[offset_data + 5] = (bytes[offset_byte + 8] >> 1 & (0x7f)) | ((bytes[offset_byte + 9] & 0x3f) << 7)
        out[offset_data + 6] = (bytes[offset_byte + 9] >> 6 & (0x03)) | ((bytes[offset_byte + 10] & 0xff) << 2) | ((bytes[offset_byte + 11] & 0x07) << 10)
        out[offset_data + 7] = (bytes[offset_byte + 11] >> 3 & (0x1f)) | ((bytes[offset_byte + 12] & 0xff) << 5)
    return out

def BS2POL2(bytes: T.Bytes) -> T.Poly:
    out = np.zeros((N,), dtype=np.uint16)
    for j in range(N//8):
        for i in range(8):
            out[j * 8 + i] = ((bytes[j] >> i) & 0x01)
    return out

def BS2POLVECp(bytes: T.Bytes, params: PARAMS) -> T.PolyVector:
    bytes = bytes.reshape((-1, P*N//8))
    out = np.zeros((params.SABER_L,N), dtype=np.uint16)
    for i in range(params.SABER_L):
        out[i, :] = BS2POLp(bytes[i, :])
    return out

def BS2POLVECq(bytes: T.Bytes, params: PARAMS) -> T.PolyVector:
    bytes = bytes.reshape((-1, Q*N//8))
    out = np.zeros((params.SABER_L,N), dtype=np.uint16)
    for i in range(params.SABER_L):
        out[i, :] = BS2POLq(bytes[i, :])
    return out

def POLq2BS(p: T.Poly) -> T.Bytes:
    out = np.zeros((Q*N//8,), dtype=np.uint8)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 8):
        offset_byte = 13 * j
        offset_data = 8 * j
        out[offset_byte + 0] = (p[offset_data + 0] & (0xff))
        out[offset_byte + 1] = ((p[offset_data + 0] >> 8) & 0x1f) | ((p[offset_data + 1] & 0x07) << 5)
        out[offset_byte + 2] = ((p[offset_data + 1] >> 3) & 0xff)
        out[offset_byte + 3] = ((p[offset_data + 1] >> 11) & 0x03) | ((p[offset_data + 2] & 0x3f) << 2)
        out[offset_byte + 4] = ((p[offset_data + 2] >> 6) & 0x7f) | ((p[offset_data + 3] & 0x01) << 7)
        out[offset_byte + 5] = ((p[offset_data + 3] >> 1) & 0xff)
        out[offset_byte + 6] = ((p[offset_data + 3] >> 9) & 0x0f) | ((p[offset_data + 4] & 0x0f) << 4)
        out[offset_byte + 7] = ((p[offset_data + 4] >> 4) & 0xff)
        out[offset_byte + 8] = ((p[offset_data + 4] >> 12) & 0x01) | ((p[offset_data + 5] & 0x7f) << 1)
        out[offset_byte + 9] = ((p[offset_data + 5] >> 7) & 0x3f) | ((p[offset_data + 6] & 0x03) << 6)
        out[offset_byte + 10] = ((p[offset_data + 6] >> 2) & 0xff)
        out[offset_byte + 11] = ((p[offset_data + 6] >> 10) & 0x07) | ((p[offset_data + 7] & 0x1f) << 3)
        out[offset_byte + 12] = ((p[offset_data + 7] >> 5) & 0xff)
    return out

def POLp2BS(p: T.Poly) -> T.Bytes:
    out = np.zeros((P*N//8,), dtype=np.uint8)
    offset_byte = 0
    offset_data = 0
    for j in range(N // 4):
        offset_byte = 5 * j
        offset_data = 4 * j
        out[offset_byte + 0] = (p[offset_data + 0] & (0xff))
        out[offset_byte + 1] = ((p[offset_data + 0] >> 8) & 0x03) | ((p[offset_data + 1] & 0x3f) << 2)
        out[offset_byte + 2] = ((p[offset_data + 1] >> 6) & 0x0f) | ((p[offset_data + 2] & 0x0f) << 4)
        out[offset_byte + 3] = ((p[offset_data + 2] >> 4) & 0x3f) | ((p[offset_data + 3] & 0x03) << 6)
        out[offset_byte + 4] = ((p[offset_data + 3] >> 2) & 0xff)
    return out

def POL22BS(p: T.Poly) -> T.Bytes:
    out = np.zeros((N//8,), dtype=np.uint8)
    for j in range(N//8):
        for i in range(8):
            out[j] = out[j] | ((p[j * 8 + i] & 0x01) << i)
    return out

def POLVECq2BS(v: T.PolyVector, params: PARAMS) -> T.Bytes:
    out = np.zeros((params.SABER_L*Q*N//8,), dtype=np.uint8)
    for i in range(params.SABER_L):
        out[i*Q*N//8:(i+1)*Q*N//8] = POLq2BS(v[i, :])
    return out

def POLVECp2BS(v: T.PolyVector, params: PARAMS) -> T.Bytes:
    out = np.zeros((params.SABER_L*P*N//8,), dtype=np.uint8)
    for i in range(params.SABER_L):
        out[i*P*N//8:(i+1)*P*N//8] = POLp2BS(v[i, :])
    return out
