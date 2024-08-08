import numpy as np
from scipy import signal
import time
import matplotlib.pyplot as plt


class FM_demod():

    def __init__(self, FSK_freq_0=70, FSK_freq_1=150, bit_rate=40):
        # Parameters
        self.path = "./Pluto_Rx.bin"
        self.samp_rate = 40000
        self.FSK_freq_0 = FSK_freq_0
        self.FSK_freq_1 = FSK_freq_1
        self.FSK_freq = (self.FSK_freq_1 - self.FSK_freq_0) / 2
        self.FM_deviation_freq = self.FSK_freq / self.samp_rate
        self.bit_rate = bit_rate
        self.sampPerBit = int(self.samp_rate / self.bit_rate)
        # self.preamble_str = "1111100110101"
        self.PRBS7_init = 1 << 6 # 1000000
        self.preamble_str = ""
        self.realInfo_period = None
        self.matchThPct = 0.9
        # self.infoLength = 16
        # self.dataLength = self.infoLength * self.sampPerBit
        self.LFSR()

    # Construct the PRBS7 sequence
    def LFSR(self):
        lfsr = self.PRBS7_init
        period = 0
        bits = []

        while True:
            # PRBS7 = x^7 + x^6 + 1
            bit = (lfsr ^ (lfsr >> 1)) & 1
            bits.append(lfsr & 1)
            lfsr = (lfsr >> 1) | (bit << 6)
            period += 1
            if lfsr == self.PRBS7_init:
                break
        
        # The info in one period
        info_period = np.array(bits, dtype=int)
        # First 16 samples as the preamble
        self.preamble_str = ''.join([str(i) for i in info_period[ : 16]])
        # The real info period
        self.realInfo_period = np.concatenate((info_period[16 : ], info_period[ : 16]), axis=0)


    def read_file(self):
        data = np.fromfile(open(self.path), dtype=np.complex64)
        data = data[500:] # First few samples are unstable
        samples = len(data)
        print('Total %d samples.'%samples)
        return data


    # Do FFT and find the carrier (max gain), and locate the FSK component, then, the useful signal is filtered
    def FFT_centralize_filter(self, x, order=4, cutoff_scale_FSK=2):
        # X-axis
        freqs = np.fft.fftshift(np.fft.fftfreq(len(x), 1/self.samp_rate))
        fft = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(x) / len(x))))

        # Center frequency
        carrier_freq = freqs[np.argmax(fft)]
        print('The carrier frequency is at %.2f Hz.'%carrier_freq)
        # Move the FSK pair to the center
        center = carrier_freq + self.FSK_freq_0 + self.FSK_freq
        n = np.arange(len(x))
        x_c = x*np.exp(-1j*2*np.pi*center/self.samp_rate*n)

        # Butterworth low-pass
        # n-order butterworth, cutoff is critical frequency normalized by sample rate
        cutoff = cutoff_scale_FSK * self.FSK_freq / self.samp_rate
        b, a = signal.butter(order, cutoff, 'lowpass')
        # Filtfilt
        y = signal.filtfilt(b, a, x_c)
        fft_y = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(y) / len(y))))
        # Crop the side of the fft, which is useless
        display_range = (self.FSK_freq+3*self.FSK_freq_0) / self.samp_rate * len(y)
        freqs = freqs[int(len(y)/2-display_range) : int(len(y)/2+display_range)]
        fft_y = fft_y[int(len(y)/2-display_range) : int(len(y)/2+display_range)]
        return y, freqs, fft_y


    def demod(self, x):
        # Extract phase of the signal
        phi = np.arctan2(np.imag(x), np.real(x))
        # Calculate frequency from phase
        y = np.diff(np.unwrap(phi))/(2*np.pi*self.FM_deviation_freq)
        return y


    # Low pass to smooth the demod result
    def smooth(self, x, order=3, cutoff_scale_bps=4):
        # n-order butterworth, cutoff is critical frequency normalized by sample rate
        cutoff = cutoff_scale_bps * self.bit_rate / self.samp_rate
        b, a = signal.butter(order, cutoff, 'lowpass')
        # Filtfilt
        y = signal.filtfilt(b, a, x)
        return y


    # Thresholding to -1 and 1
    def threshold(self, x):
        y = np.zeros_like(x)
        y[x<0] = -1
        y[x>=0] = 1
        return y


    # Mathched filter to detect the data, singal is a set of [-1,1], not [0,1]
    # Only calculate preamble for matching, followed by the fix datalength, more efficient for calculating
    def matched_pre_dataLength(self, x):
        # Design the matched filter
        preamble = np.array([int(i) for i in self.preamble_str])
        # Replace the 0 with -1 to gain maximum correlation
        preamble[preamble==0] = -1
        # Repeat and flip
        preamble = np.repeat(preamble, self.sampPerBit)
        matchFilter_pre = np.flip(preamble)
        # Do the convolution
        cov_pre = np.convolve(x, matchFilter_pre, 'valid')

        # Find the value meet the matched
        matchedWell_pre = len(preamble)
        match_pre = np.where(cov_pre > self.matchThPct * matchedWell_pre)[0]

        # plt.figure()
        # plt.plot(cov_pre, label='Signal')
        # ideal = np.ones_like(cov_pre) * matchedWell_pre
        # th = np.ones_like(cov_pre) * matchedWell_pre * self.matchThPct
        # th_l = np.ones_like(cov_pre) * -self.sampPerBit
        # th_h = np.ones_like(cov_pre) * self.sampPerBit
        # plt.plot(ideal, 'g', label='Ideal match')
        # plt.plot(th, 'r', label='Threshold = 0.9')
        # plt.plot(th_l, 'm', label='R(n) = -1')
        # plt.plot(th_h, 'y', label='R(n) = 1')
        # plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0)
        # plt.subplots_adjust(right=0.75)
        # plt.ylabel('Correlation')
        # plt.grid()
        # plt.title('Correlation between the received signal and the preamble')
        # plt.show()

        if match_pre.size > 0:
            # Loop till find the data
            while True:
                # Find the max in the next range(sampPerBit)
                max_pre = np.max(cov_pre[match_pre[0]: match_pre[0] + self.sampPerBit])
                # Index of matched
                maxIndex_pre = np.argmax(cov_pre[match_pre[0]: match_pre[0] + self.sampPerBit]) + match_pre[0]

                if max_pre > self.matchThPct * matchedWell_pre: # Preamble matched
                    print('Well matched: %d, max_pre: %d.'%(matchedWell_pre, max_pre))

                    # Calculate the starting point
                    startIndex = maxIndex_pre + len(preamble)
                    if len(x)-startIndex > 1.5*self.sampPerBit: # Data exist
                        return True, x[startIndex:-1]
                    else: # No data
                        return False, x
                    
                else: # Not a matched preamble
                    match_pre = np.delete(match_pre, match_pre < maxIndex_pre)
                    if match_pre.size > 0:
                        continue
                    else: # Already loop all matching postamble but no satisfied
                        return False, x
                    
        else: # No match
            return False, x


    # Extract info from data
    def extract_info(self, x):
        # Take the differential to get the edge
        x_diff = np.diff(x)
        edgesIndex = np.where(x_diff != 0)[0]
        if edgesIndex[0] < 0.1*self.sampPerBit: # Noise
            edgesIndex = np.delete(edgesIndex, 0)

        info = np.array([])
        # First same bits
        value = x_diff[edgesIndex[0]] * -0.5
        bits = (edgesIndex[0] + 0.5*self.sampPerBit) // self.sampPerBit
        info = np.append(info, np.repeat(value, bits))

        ### Edge range decoding ###
        i = 1 # Index of edge
        while True:
            # Same bits
            value = x_diff[edgesIndex[i]] * -0.5
            bits = (edgesIndex[i] - edgesIndex[i-1] + 0.5*self.sampPerBit) // self.sampPerBit
            info = np.append(info, np.repeat(value, bits))
            if edgesIndex[i] == edgesIndex[-1]: # At the last edge
                break
            else:
                i += 1
        ### Edge range decoding ###

        # ### Adaptive bit rate decoding ###
        # # Estimate the sample per bit (inversely proportional to bit rate)
        # sampPerBit_est = int(edgesIndex[0] / bits)
        # i = 1 # Index of edge
        # while True:
        #     j = 0 # Index of bit between edges
        #     while True:
        #         # Take the average according to the sampPerBit_est
        #         value = np.average(x[int(edgesIndex[i-1]+1 + j*sampPerBit_est) : int(edgesIndex[i-1]+1 + (j+1)*sampPerBit_est)])
        #         value = 1 if value >= 0 else -1
        #         info = np.append(info, value)
        #         # Judge if meet the edge
        #         if (edgesIndex[i-1]+1 + (j+1)*sampPerBit_est + 0.5*sampPerBit_est) >= edgesIndex[i]:
        #             break
        #         else:
        #             j += 1

        #     # Update the sampPerBit_est
        #     sampPerBit_est = (edgesIndex[i] - edgesIndex[i-1]) / (j+1)
        #     # Judge if goes to the last edge
        #     if edgesIndex[i] == edgesIndex[-1]:
        #         # Last few bits
        #         for j in range(int((len(x)-(edgesIndex[-1]+1)) // sampPerBit_est)):
        #             value = np.average(x[int(edgesIndex[i]+1 + j*sampPerBit_est) : int(edgesIndex[i]+1 + (j+1)*sampPerBit_est)])
        #             value = 1 if value >= 0 else -1
        #             info = np.append(info, value)
        #         break
        #     else:
        #         i += 1
        # ### Adaptive bit rate decoding ###

        info[info==-1] = 0
        info = info.astype(int)
        return info


    # Calulate BER
    # Real info is PRBS7 = x^7 + x^6 + 1
    def BER(self, info):
        # Construct real info
        infoLength = len(info)
        realInfo = np.tile(self.realInfo_period, int(infoLength / len(self.realInfo_period)))
        realInfo = np.concatenate((realInfo, self.realInfo_period[: (infoLength % len(self.realInfo_period))]), axis=0)
        # Calulate BER
        berPct = np.sum(info != realInfo) / infoLength * 100
        if berPct > 0:
            firstError = np.where(info != realInfo)[0][0] + 1
        else:
            firstError = 0
        return infoLength, berPct, firstError


def main():
    
    FSK_freq_0 = int(input('FSK freqency #0:\n'))
    FSK_freq_1 = int(input('FSK freqency #1:\n'))
    bit_rate = int(input('Bit rate:\n'))

    startTime = time.time()

    fm = FM_demod(FSK_freq_0, FSK_freq_1, bit_rate)

    original = fm.read_file()
    filteredData, freqs, fft = fm.FFT_centralize_filter(original)
    signalData = fm.demod(filteredData)
    signalData_smooth = fm.smooth(signalData)
    signalData_th = fm.threshold(signalData_smooth)
    isMatched, data = fm.matched_pre_dataLength(signalData_th)
    if isMatched:
        print('Matched!')
        info = fm.extract_info(data)
        infoLength, berPct, firstError = fm.BER(info)
        print('Bit legth: %d\nBER: %.4f%%\nFirst error occur on Bit #%d (0 means no error).'%(infoLength, berPct, firstError))
    else:
        print('Mismatched!')

    endTime = time.time()
    print('Time spent: %.2fs.\n\n' % (endTime-startTime))

    # Plot
    plt.figure(0)
    plt.subplot(321)
    plt.plot(np.real(original), label='real')
    plt.plot(np.imag(original), label='imag')
    plt.legend()
    plt.grid()
    plt.title('Original')

    plt.subplot(323)
    plt.plot(freqs, fft)
    plt.xlabel('Hz')
    plt.ylabel('dB')
    plt.grid()
    plt.title('FFT')

    plt.subplot(325)
    plt.plot(signalData)
    plt.ylim([-10, 10])
    plt.grid()
    plt.title('FM Demod')

    plt.subplot(322)
    plt.plot(signalData_smooth)
    plt.ylim([-5, 5])
    plt.grid()
    plt.title('Smooth')

    plt.subplot(324)
    plt.plot(signalData_th)
    plt.ylim([-1.5, 1.5])
    plt.grid()
    plt.title('Thresholding')

    plt.subplot(326)
    plt.plot(data)
    plt.ylim([-1.5, 1.5])
    plt.grid()
    plt.title('Info Data (if matched)')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
