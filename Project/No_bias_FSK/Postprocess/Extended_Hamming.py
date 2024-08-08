# 海明码（Hamming Code）：基于矩阵思路的一些理解
# https://blog.csdn.net/weixin_57915039/article/details/117523933

# 数字传输 | 任意位数的汉明码hamming code编码+产生误差+纠错（原理+python代码实现）
# https://blog.csdn.net/Yizkkkkang/article/details/117512451

# First, calculate the length of the codeword according to the info bit.
#     r: parity check bit
#     n = 2^r - 1
#     k = 2^r - 1 - r
#     Thus, info bit <= 2^r - 1 - r, so determine r, then, n.
 
# Then, generate the parity-check matrix according H to the total codeword length.
#     See from the column, from left to right is the binary of the number from 1 to 2^r - 1.
#     The 2^i columns only have one 1.
#     Top is LSB, bottom is MSB. E.g. r=3, 100, 010, 110, 001, 101, 011, 111. (1,2,4 columns have one 1)

# Next, determine the generator matrix G from the parity-check matrix H.
#     Delete the 2^i columns of H matrix, denoted A.
#     Generate a k*k identical matrix, denoted B.
#     Insert each row of A to B at row 2^i.
#     That is, after inserting, the 2^i rows are each row of A, others are the k*k identical matrix.
#     Last, transpose and get G matrix.

# Finally, add one more parity check bit to form extended Hamming code.
#     For G matrix, at the last column, add a even parity check bit.
#     For H matrix,
#     First add zeros at the last column (the additional bit does not play a role in normal Hamming code).
#     Then, add ones at the last row (even parity check rule).

# Convert to system code if necessary




import numpy as np
import pandas as pd

def length_codeword(info_length):
    par_bits = 0
    # Info bit <= 2^r - 1 - r
    while(info_length > 2**par_bits - par_bits - 1):
        par_bits += 1
    
    total_bits = 2**par_bits - 1
    info_bits = 2**par_bits - par_bits - 1
    print('Number of parity bits: %d+1.\nNumber of info bits: %d.\nNumber of total bits: %d.\n' % (par_bits, info_bits, total_bits))
    return info_bits, total_bits


def H(total_bits):
    column = [] 
    j = -1
    for i in range(1, total_bits+1):
        num = bin(i) # Convert to binary string e.g. '0b1010'
        while num[j] != "b":
            column += num[j]
            j -= 1
        j = -1

        column = list(map(int, column))  
        if i==1:
            col = pd.DataFrame(column, columns=['1'])
        else:
            column = pd.DataFrame(column, columns=[str(i)])
            H_dataframe = pd.concat([col,column], axis=1)
            col = H_dataframe
        column = []
        
    H_dataframe.fillna(0, inplace=True) # Fill 0s at Nan
    H_dataframe.index = H_dataframe.index + 1 # Index start from 1
    return H_dataframe


def G(H_dataframe, info_bits, total_bits):
    # Identical matrix
    unit_matrix = np.eye(info_bits)

    # Drop
    h_dataframe = H_dataframe.copy()
    for i in range(1, total_bits+1):
        if i & i-1 == 0: # i == 2^n
            h_dataframe.drop(str(i), axis=1, inplace=True)
    g_dataframe = h_dataframe

    # Insert
    j = 0
    for i in range(1, total_bits+1):
        if i & i-1 == 0:
            G_matrix = np.insert(unit_matrix, i-1, g_dataframe.iloc[j], axis=0)
            unit_matrix = G_matrix
            j += 1

    G_matrix = G_matrix.T
    return G_matrix


def extend(G_matrix, H_matrix):
    par_bit = np.sum(G_matrix, axis=1).reshape(-1, 1) % 2
    G_matrix_ex = np.concatenate((G_matrix, par_bit), axis=1)

    H_matrix_ex = np.concatenate((H_matrix, np.zeros((H_matrix.shape[0], 1))), axis=1)
    H_matrix_ex = np.concatenate((H_matrix_ex, np.ones((1, H_matrix_ex.shape[1]))), axis=0)

    return G_matrix_ex, H_matrix_ex


def system_code(G_matrix_ex, H_matrix_ex):
    def column_sort(matrix, order):
        sort_matrix = matrix.copy()
        for i in range(matrix.shape[1]):
            sort_matrix[:, i] = matrix[:, order[i]]
        return sort_matrix
    
    # Find the info bit
    row_combine = np.sum(G_matrix_ex, axis=0)
    info_index = np.where(row_combine == 1)[0]
    
    # Sort the info bit
    order = np.zeros(info_index.size, dtype=int)
    for i in info_index:
        index = (np.where(G_matrix_ex[:, i] == 1)[0][0])
        order[index] = i
    
    # Full order
    for i in range(G_matrix_ex.shape[1]):
        if i not in order:
            order = np.append(order, i)

    # Resort
    G_matrix_sys = column_sort(G_matrix_ex, order)
    H_matrix_sys = column_sort(H_matrix_ex, order)
    return G_matrix_sys, H_matrix_sys


def row_with_comma(matrix):
    rows = '['
    for i in range(matrix.shape[0]):
        row = ','.join(str(k) for k in matrix[i, :])
        row = '[' + row + '],\n'
        rows += row
    # Crop the last comma and add a ]
    rows = rows[:-2]
    rows += ']'
    return rows


def main():
    # The bit of info
    k = 26

    info_bits, total_bits = length_codeword(k)
    H_dataframe = H(total_bits)
    G_matrix = G(H_dataframe, info_bits, total_bits)
    H_matrix = np.array(H_dataframe)
    G_matrix_ex, H_matrix_ex = extend(G_matrix, H_matrix)
    G_matrix_sys, H_matrix_sys = system_code(G_matrix_ex, H_matrix_ex)
    
    G_matrix_sys = G_matrix_sys.astype(int)
    H_matrix_sys = H_matrix_sys.astype(int)
    G_matrix_comma = row_with_comma(G_matrix_sys)
    H_matrix_comma = row_with_comma(H_matrix_sys)

    print('G matrix', G_matrix_comma, sep='\n')
    print()
    print('H matrix', H_matrix_comma, sep='\n')


if __name__ == '__main__':
    main()


# G = np.array(  [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1],
#                 [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1], 
#                 [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1], 
#                 [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0], 
#                 [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1], 
#                 [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1], 
#                 [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0], 
#                 [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1], 
#                 [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,0],
#                 [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0],
#                 [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,1,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,1,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,1],
#                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0]])

# H = np.array(  [[1,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0,0],
#                 [1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0,0],
#                 [0,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0,0],
#                 [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1,0,0],
#                 [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,0],
#                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]])

# H_noExtend = np.array( [[1,1,0,1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0],
#                         [1,0,1,1,0,1,1,0,0,1,1,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,0,0],
#                         [0,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,0,0],
#                         [0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1,0],
#                         [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1]])

# m = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1, 0,0,0,0,0,1,1,0,1,0]) # Addr: 1, temp: 26

# c = np.dot(m, G) % 2
# print(c)
