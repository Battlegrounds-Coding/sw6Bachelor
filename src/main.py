"THIS IS THE MAIN FILE"

from datetime import datetime
from python_package.cash.cash import FileCash, CashData
import numpy as np


f = FileCash('./file.cash')
f.insert(CashData(datetime.now(), [np.float64(4), np.float64(3)]))
print(f.get(14).time)




