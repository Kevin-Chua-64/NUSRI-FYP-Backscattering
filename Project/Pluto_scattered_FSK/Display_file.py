import numpy as np
import matplotlib.pyplot as plt

data = np.fromfile(open("FSK_Demod.bin"), dtype=np.complex64)
samples = len(data)
print('Total %d samples.'%samples)

plt.figure(0)
plt.plot(data)
plt.show()
