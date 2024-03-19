"THIS IS THE MAIN FILE"

import numpy as np
from python_package.result import Ok

print(Ok(3).value())


MSG = "Roll a dice"
print(MSG)

print(np.random.randint(1, 9))
