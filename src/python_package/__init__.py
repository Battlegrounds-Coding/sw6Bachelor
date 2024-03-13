"""Python Package Template"""

from __future__ import annotations

__version__ = "0.0.2"

import numpy as np
from result import Ok

print(Ok(3).value())


MSG = "Roll a dice"
print(MSG)

print(np.random.randint(1, 9))
