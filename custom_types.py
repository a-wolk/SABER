import numpy.typing as npt
import numpy as np
from typing import Tuple

PolyMatrix = npt.NDArray[np.uint16] # shape = (L, L, N)
PolyVector = npt.NDArray[np.uint16] # shape = (L, N)
Poly = npt.NDArray[np.uint16] # shape = (N,)

Bytes = npt.NDArray[np.uint8]

PublicKey = Tuple[Bytes, Bytes]