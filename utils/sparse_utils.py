import numpy as np
import scipy.sparse as sparse


def multiply_row(A, row_idx, alpha):
    '''
    multiply values in row_idx in place 
    '''
    idx_start_row = A.indptr[row_idx]
    idx_end_row = A.indptr[row_idx + 1]

    A.data[idx_start_row:idx_end_row] = (alpha *
                                         A.data[idx_start_row:idx_end_row]
                                         )


def multiply_col(A, col_idx, alpha):
    '''
    multiply values in col_idx in place 
    '''
    col_indices = A.indices == col_idx
    A.data[col_indices] = (alpha * A.data[col_indices])
