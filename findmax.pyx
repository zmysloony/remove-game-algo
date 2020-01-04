import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.

def find_to_none(nums, long[:] gains):
    cdef int i = 0
    cdef int lens = len(nums)
    cdef maxgain
    while nums[i] is None and i < lens:
        i += 1
    maxgain = gains[i]
    maxindices = []

    while i < lens and nums[i] is not None:
        if gains[i] > maxgain:
            maxgain = gains[i]
            maxindices = []
        if gains[i] == maxgain:
            maxindices.append(i)
        i += 1
    return maxindices
