# taps: 16 15 13 4; feedback polynomial: x^16 + x^15 + x^13 + x^4 + 1
# bit = (lfsr ^ (lfsr >> 1) ^ (lfsr >> 3) ^ (lfsr >> 12)) & 1

# PRBS7 = x^7 + x^6 + 1
# bit = (lfsr ^ (lfsr >> 1)) & 1

start_state = 1 << 6 # 1000000
lfsr = start_state
period = 0
bits = []

while True:
    bit = (lfsr ^ (lfsr >> 1)) & 1
    bits.append(lfsr & 1)
    lfsr = (lfsr >> 1) | (bit << 6)
    period += 1
    if lfsr == start_state:
        print(period)
        break

print('PRBS7, start state 1000000:', bits, sep='\n')
