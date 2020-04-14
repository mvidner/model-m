import numpy as np
import scipy.sparse as sparse


def multiply_row(A, row_idx, alpha, trunc=False):
    '''
    multiply values in row_idx in place 
    '''
    idx_start_row = A.indptr[row_idx]
    idx_end_row = A.indptr[row_idx + 1]

    A.data[idx_start_row:idx_end_row] = (alpha *
                                         A.data[idx_start_row:idx_end_row]
                                         )
    if trunc:
        A.data[idx_start_row:idx_end_row] = np.clip(A.data[idx_start_row:idx_end_row], 0.0, 1.0)


def multiply_col(A, col_idx, alpha, trunc=False):
    '''
    multiply values in col_idx in place 
    '''
    col_indices = A.indices == col_idx
    A.data[col_indices] = (alpha * A.data[col_indices])
    if trunc:
        A.data[col_indices] = np.clip(A.data[col_indices], 0.0, 1.0)

def multiply_zeros_as_ones(a, b):
    c = a.minimum(b)
    r, c = c.nonzero()

    data = np.ones(len(r))
    ones = sparse.csr_matrix((data, (r, c)), shape=a.shape)

    # get common elements
    ones_a = ones.multiply(a)
    ones_b = ones.multiply(b)

    a_dif = a - ones_a
    b_dif = b - ones_b

    result = ones_a.multiply(ones_b)
    return result + a_dif + b_dif
