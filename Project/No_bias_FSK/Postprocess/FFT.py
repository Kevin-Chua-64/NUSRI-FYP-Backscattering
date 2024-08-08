import numpy as np
import matplotlib.pyplot as plt

# Parameters
samp_rate = 40000
bit_rate = 20
sampPerBit = int(samp_rate / bit_rate)
FFT_size = 65536

# Read file
data = np.fromfile(open("./Pluto_Rx.bin"), dtype=np.complex64)
samples = len(data)
print('Total %d samples.'%samples)

# # FFT
# freqs = np.fft.fftshift(np.fft.fftfreq(FFT_size, 1/samp_rate))
# f = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(data[1000 + 3*FFT_size:], FFT_size) / FFT_size)))

# FFT
freqs = np.fft.fftshift(np.fft.fftfreq(FFT_size, 1/samp_rate))
f = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(data[1000 + 2*sampPerBit:], FFT_size) / sampPerBit)))


# Plot
plt.figure(0)
plt.plot(freqs, f)
plt.xlabel('Hz')
plt.ylabel('dB')
plt.grid()
plt.show()
