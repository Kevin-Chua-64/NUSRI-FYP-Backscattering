# BER vs. bit SNR for non-coherent FSK
# P_b approximately = 0.5 * e^(-SNR/2)

import numpy as np
import matplotlib.pyplot as plt

SNR_dB = np.linspace(-5, 15, 2001)
SNR = 10**(SNR_dB/10)

P_b = 0.5 * np.exp(-SNR/2)

plt.figure()
plt.plot(SNR_dB, np.log10(P_b))
plt.xlabel('Bit SNR (dB)')
plt.ylabel('log(BER)')
plt.title('BER vs. bit SNR')
plt.grid()
plt.show()
