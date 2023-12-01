import hashlib
import numpy as np
import numpy.typing as npt

def shake128(_bytes: npt.NDArray[np.uint8], n: int) -> npt.NDArray[np.uint8]:
    _bytes = bytes(_bytes.tolist())
    _bytes = hashlib.shake_128(_bytes).digest(n)
    return np.array(list(_bytes), dtype=np.uint8)
