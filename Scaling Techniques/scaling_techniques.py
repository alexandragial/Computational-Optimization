import numpy as np
import math

""" Geometric Mean """

def geometric_mean_scaling(A, b, c):
  m, n = A.shape

  #For columns
  colmax = list()
  colmin = list()
  mc = list()

  for col in range(n):
    colmax.append(np.max(np.abs(A[:, col])))
    colmin.append(np.min(np.abs(A[:, col])))
    mc.append(math.sqrt(colmax[col] * colmin[col]))
    A[:, col] = A[:, col] / mc[col]
    c[col] = c[col] / mc[col]

  #For rows
  rowmax = list()
  rowmin = list()
  mr = list()

  for row in range(m):
    rowmax.append(np.max(np.abs(A[row])))
    rowmin.append(np.min(np.abs(A[row])))
    mr.append(math.sqrt(rowmax[row] * rowmin[row]))
    A[row] = A[row] / mr[row]
    b[row] = b[row] / mr[row]

  return A, b, c

""" Arithmetic Mean """

def arithmetic_mean_scaling(A, b, c):
  m, n = A.shape

  r = list()
  for row in range(m):
    r.append(np.count_nonzero(A[row]) / np.sum(np.abs(A[row])))
    A[row] = A[row] * r[row]
    b[row] = b[row] * r[row]

  s = list()
  for col in range(n):
    s.append(np.count_nonzero(A[:, col]) / np.sum(np.abs(A[:, col])))
    A[:, col] = A[:, col] * s[col]
    c[col] = c[col] * s[col]

  return A, b, c

# Printing results
scaled_A, scaled_b, scaled_c = arithmetic_mean_scaling(A, b, c)
print("Array A after scaling\n", scaled_A, "\n")
print("Array b after scaling\n", scaled_b, "\n")
print("Array c after scaling\n", scaled_c, "\n")