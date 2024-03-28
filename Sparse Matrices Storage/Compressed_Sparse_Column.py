import numpy as np

arr = np.array([[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 4, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 8, 0, 0, 0],
             [0, 0, 0, 0, 0, 3],
             [0, 0, 0, 0, 0, 0]])

rows, cols = arr.shape
anz, ia, ja = [], [], []
index = 0
countNz = 0

for j in range(cols):
    serialNum = 0
    for i in range(rows):
        if arr[i][j] == 0:
            if i == rows - 1 and np.all((arr[:,j] == 0)):
                ia.append(0)
        if arr[i][j] != 0:
            serialNum += 1
            countNz += 1
            anz.append(arr[i][j])
            ja.append(i + 1)
            if serialNum == 1:
                if len(ja) > 0:
                    for index in range(len(ia)):
                        if ia[index] == 0:
                            ia[index] = countNz
                ia.append(countNz)
        if i == rows - 1 and j == cols - 1:
            if all(values == 0 for values in ia):
                ia = [1 for i in range(len(ia)+1)]
            else:
                for index in range(len(ia)):
                    if ia[index] == 0:
                        ia[index] = countNz+1
                ia.append(countNz + 1)

print("Number of non-zero elements:", countNz)
print("Anz =", anz)
print("JA =", ja)
print("IA =", ia)