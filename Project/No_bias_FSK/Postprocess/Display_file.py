import numpy as np
import matplotlib.pyplot as plt

data = np.fromfile(open("./Pluto_Rx.bin"), dtype=np.complex64)
samples = len(data)
print('Total %d samples.'%samples)

plt.figure(0)
plt.plot(np.real(data), label='real')
plt.plot(np.imag(data), label='imag')
plt.legend()
plt.ylim([-1.5, 1.5])
plt.grid()
plt.show()
