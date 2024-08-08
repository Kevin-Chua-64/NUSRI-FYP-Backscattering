import numpy as np
from scipy import signal
import time
import socket
import matplotlib.pyplot as plt


class FM_demod():

    def __init__(self):
        # Parameters
        self.path = "./Pluto_Rx.bin"
        self.samp_rate = 40000
        self.FSK_freq_0 = 70
        self.FSK_freq_1 = 150
        self.FSK_freq = (self.FSK_freq_1 - self.FSK_freq_0) / 2
        self.FM_deviation_freq = self.FSK_freq / self.samp_rate
        self.bit_rate = 40
        self.sampPerBit = int(self.samp_rate / self.bit_rate)
        self.preamble_str = "1111100110101"
        self.postamble_str = "11100010010"
        self.matchThPct = 0.9
        self.infoLength = 32
        self.dataLength = self.infoLength * self.sampPerBit


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
    def matched_pre_post(self, x):
        # Design the matched filter
        preamble = np.array([int(i) for i in self.preamble_str])
        postamble = np.array([int(i) for i in self.postamble_str])
        # Replace the 0 with -1 to gain maximum correlation
        preamble[preamble==0] = -1
        postamble[postamble==0] = -1
        # Repeat and flip
        preamble = np.repeat(preamble, self.sampPerBit)
        postamble = np.repeat(postamble, self.sampPerBit)
        matchFilter_pre = np.flip(preamble)
        matchFilter_post = np.flip(postamble)
        # Do the convolution
        cov_pre = np.convolve(x, matchFilter_pre, 'valid')
        cov_post = np.convolve(x, matchFilter_post, 'valid')

        # Find the value meet the matched
        matchedWell_pre = len(preamble)
        matchedWell_post = len(postamble)
        match_pre = np.where(cov_pre > self.matchThPct * matchedWell_pre)[0]
        match_post = np.where(cov_post > self.matchThPct * matchedWell_post)[0]

        if match_pre.size > 0 and match_post.size > 0:
            # Loop till find the data
            while True:
                # Find the max in the next range(sampPerBit)
                max_pre = np.max(cov_pre[match_pre[0]: match_pre[0] + self.sampPerBit])
                max_post = np.max(cov_post[match_post[0]: match_post[0] + self.sampPerBit])
                # Index of matched
                maxIndex_pre = np.argmax(cov_pre[match_pre[0]: match_pre[0] + self.sampPerBit]) + match_pre[0]
                maxIndex_post = np.argmax(cov_post[match_post[0]: match_post[0] + self.sampPerBit]) + match_post[0]

                if max_pre > self.matchThPct * matchedWell_pre: # Preamble matched
                    if max_post > self.matchThPct * matchedWell_post: # Postamble matched
                        print('Pre well matched: %d, max_pre: %d.\nPost well matched: %d, max_post: %d.'%(matchedWell_pre, max_pre, matchedWell_post, max_post))

                        if maxIndex_pre < maxIndex_post: # Preamble must before postamble
                            # Calculate the starting and ending point
                            startIndex = maxIndex_pre + len(preamble)
                            endIndex = maxIndex_post-1
                            if np.abs(((endIndex+1)-startIndex) - self.dataLength) < self.sampPerBit: # Good
                                return True, x[startIndex:endIndex+1]
                            else: # Data length not fit, bad matched, re-calculate preamble
                                match_pre = np.delete(match_pre, match_pre < maxIndex_pre + self.sampPerBit)
                                if match_pre.size > 0:
                                    continue
                                else: # Already loop all matching preamble but no satisfied
                                    return False, x

                        else: # Postamble before preamble, re-calculate postamble
                            match_post = np.delete(match_post, match_post < maxIndex_post + self.sampPerBit)
                            if match_post.size > 0:
                                continue
                            else: # Already loop all matching postamble but no satisfied
                                return False, x
                            
                    else: # Not a matched postamble
                        match_post = np.delete(match_post, match_post < maxIndex_post)
                        if match_post.size > 0:
                            continue
                        else: # Already loop all matching postamble but no satisfied
                            return False, x
                        
                else: # Not a matched preamble
                    match_pre = np.delete(match_pre, match_pre < maxIndex_pre)
                    if match_pre.size > 0:
                        continue
                    else: # Already loop all matching postamble but no satisfied
                        return False, x
                    
        else: # No match
            return False, x


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

                    # Calculate the starting and ending point
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
        
        # Edge range decoding
        i = 1 # Index of edge
        while True:
            # Same bits
            value = x_diff[edgesIndex[i]] * -0.5
            bits = (edgesIndex[i] - edgesIndex[i-1] + 0.5*self.sampPerBit) // self.sampPerBit
            info = np.append(info, np.repeat(value, bits))
            if edgesIndex[i] == edgesIndex[-1] or info.size >= self.infoLength: # At the last edge or meet the info length
                if info.size < self.infoLength: # Data is not fully transmitted
                    return False, info
                elif info.size > self.infoLength: # Beyond size, crop
                    info = info[:self.infoLength]
                    break

            else:
                i += 1

        info[info==-1] = 0
        info = info.astype(int)
        return True, info
        

    # Deocde the info (extended Hamming code, (31+1, 26))
    # decoded info = [16-bit address, 10-bit temperature]
    def Hamming_decode(self, info, info_bits=26, addr_bits=16, H=
                       np.array([[1,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0],
                                 [1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0],
                                 [0,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0],
                                 [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1,0],
                                 [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1]])):
        # Decode
        # Parity check
        par_flag = None
        if np.sum(info[:-1])%2 == info[-1]:
            par_flag = True # Correct
        else:
            par_flag = False

        # Hamming one-bit correct
        ham_flag = None
        # Syndrom vector
        s = np.dot(info[:-1], H.T) % 2
        if np.sum(s, axis=0) == 0:
            ham_flag = True # Correct
        else:
            ham_flag = False
        
        # Verify
        if par_flag and ham_flag: # Most likely correct
            de_info = info[:info_bits]
        elif par_flag and not ham_flag: # Even bits error
            return False, info, 'None'
        elif not par_flag and ham_flag: # Odd bits error, more than 1-bit
            return False, info, 'None'
        elif not par_flag and not ham_flag: # Most likely 1-bit error, correct it
            # Find the matched syndrom (in columns)
            s_cols = np.where(H.T == s)[0]
            error_bit = np.argmax(np.bincount(s_cols))
            # Correct
            de_info = info.copy()
            de_info[error_bit] = (de_info[error_bit] + 1) % 2
            de_info = de_info[:info_bits]

        # Separate address and temperature
        addr = de_info[0:addr_bits]
        temp_sign = de_info[addr_bits]
        temp = de_info[addr_bits+1 : info_bits]
        # Convert into number
        addr_str = ''.join([str(i) for i in addr])
        temp_str = ''.join([str(i) for i in temp])
        addr_D_str = str(int(addr_str, 2))
        if temp_sign == 0: # Positive temperature
            temp_D_str = str(int(temp_str, 2))
        elif temp_sign == 1: # Negative temparature
            temp_D_str = str(int(temp_str, 2) - 2**(info_bits - addr_bits - 1))

        message = addr_D_str + ' ' + temp_D_str
        return True, de_info, message
        

# Send the info via UDP
def udpSend(message, serverName='localhost', serverPort=12000):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    clientSocket.close()


def main():
        
    startTime = time.time()

    fm = FM_demod()

    original = fm.read_file()
    filteredData, freqs, fft = fm.FFT_centralize_filter(original)
    signalData = fm.demod(filteredData)
    signalData_smooth = fm.smooth(signalData)
    signalData_th = fm.threshold(signalData_smooth)
    # isMatched, data = fm.matched_pre_post(signalData_th)
    isMatched, data = fm.matched_pre_dataLength(signalData_th)
    if isMatched:
        print('Matched!')
        isInfo, info = fm.extract_info(data)
        if isInfo:
            isNoError, de_info, message = fm.Hamming_decode(info)
            if isNoError:
                udpSend(message)
                print('Info:', de_info)
            else:
                # udpSend('None')
                print('More than 1-bit error, the codeword:', de_info)
        else:
            # udpSend('None')
            print('Info incomplete!')
            print('Incomplete info:', info)
    else:
        # udpSend('None')
        print('Mismatched!')

    endTime = time.time()
    print('Time spent: %.2fs.\n\n' % (endTime-startTime))


    # # Plot
    # plt.figure(0)
    # plt.subplot(321)
    # plt.plot(np.real(original), label='real')
    # plt.plot(np.imag(original), label='imag')
    # plt.legend()
    # plt.grid()
    # plt.title('Original')

    # plt.subplot(323)
    # plt.plot(freqs, fft)
    # plt.xlabel('Hz')
    # plt.ylabel('dB')
    # plt.grid()
    # plt.title('FFT')

    # plt.subplot(325)
    # plt.plot(signalData)
    # plt.ylim([-10, 10])
    # plt.grid()
    # plt.title('FM Demod')

    # plt.subplot(322)
    # plt.plot(signalData_smooth)
    # plt.ylim([-5, 5])
    # plt.grid()
    # plt.title('Smooth (Butterworth)')

    # plt.subplot(324)
    # plt.plot(signalData_th)
    # plt.ylim([-1.5, 1.5])
    # plt.grid()
    # plt.title('Thresholding')

    # plt.subplot(326)
    # plt.plot(data)
    # plt.ylim([-1.5, 1.5])
    # plt.grid()
    # plt.title('Info Data (if matched)')

    # plt.tight_layout()
    # plt.show()


if __name__ == '__main__':
    main()
