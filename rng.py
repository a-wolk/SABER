import numpy as np
import numpy.typing as npt

def randombytes(n: int) -> npt.NDArray[np.uint8]:
    return np.random.randint(0, 2**8, size=(n,))
