import numpy as np
import numpy.typing as npt
import custom_types as T
from constants import N, Q, P


def BS2POLq(bytes: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint16]:
    out = np.zeros((N,), dtype=np.uint16)

    bytes_last = Q*N//8-1
    for i in range(N):
        start_byte = bytes_last - (i*Q) // 8
        start_offset = (i*Q) % 8
        end_byte = bytes_last - ((i+1)*Q) // 8
        end_offset = 8 - ((i+1)*Q) % 8
        is_3_bytes = (start_byte - end_byte) > 1
        
        out[i] = (bytes[start_byte] & (0xff << start_offset)) >> start_offset
        out[i] |= (bytes[start_byte-1] << (8-start_offset)) if is_3_bytes else 0
        out[i] |= (bytes[end_byte] & (0xff >> end_offset)) << ((8-start_offset) + 8*is_3_bytes)
    return out

def BS2OLVECq(bytes: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint16]:
    l = bytes.shape[0]
    out = np.zeros((l,N), dtype=np.uint16)
    for i in range(l):
        out[i, :] = BS2POLq(bytes[l-i-1, :])
    return out

def POLq2BS(p: T.Poly) -> npt.NDArray[np.uint8]:
    out = np.zeros((Q*N//8,), dtype=np.uint8)

    bytes_last = Q*N//8-1
    for i in range(N):
        start_byte = bytes_last - (i*Q) // 8
        start_offset = (i*Q) % 8
        end_byte = bytes_last - ((i+1)*Q) // 8
        end_offset = 8 - ((i+1)*Q) % 8
        is_3_bytes = (start_byte - end_byte) > 1

        out[end_byte] |= ((p[i] & 0xff00) >> (8 + (8 - end_offset)))
        out[end_byte+1] |= ((p[i] >> start_offset) & 0xff) if is_3_bytes else 0
        out[start_byte] |= ((p[i] & (0xff >> start_offset)) << start_offset)
    return out

def POLVECq2BS(v: T.PolyVector) -> npt.NDArray[np.uint8]:
    l = v.shape[0]
    out = np.zeros((l*Q*N//8,), dtype=np.uint8)
    for i in range(l):
        out[i*Q*N//8:(i+1)*Q*N//8] = POLq2BS(v[i, :])
    return out

def POLp2BS(p: T.Poly) -> npt.NDArray[np.uint8]:
    out = np.zeros((P*N//8,), dtype=np.uint8)

    bytes_last = P*N//8-1
    for i in range(N):
        start_byte = bytes_last - (i*P) // 8
        start_offset = (i*P) % 8
        end_byte = bytes_last - ((i+1)*P) // 8
        end_offset = 8 - ((i+1)*P) % 8
        is_3_bytes = (start_byte - end_byte) > 1

        out[end_byte] |= ((p[i] & 0xff00) >> (8 + (8 - end_offset)))
        out[end_byte+1] |= ((p[i] >> start_offset) & 0xff) if is_3_bytes else 0
        out[start_byte] |= ((p[i] & (0xff >> start_offset)) << start_offset)
    return out

def POLVECp2BS(v: T.PolyVector) -> npt.NDArray[np.uint8]:
    l = v.shape[0]
    out = np.zeros((l*P*N//8,), dtype=np.uint8)
    for i in range(l):
        out[i*P*N//8:(i+1)*P*N//8] = POLp2BS(v[i, :])
    return out