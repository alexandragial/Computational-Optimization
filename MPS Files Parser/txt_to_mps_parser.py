import numpy as np

def writeMps(mpFilename, A, b, c, varName, constType, constName):
    with open(mpFilename, 'w') as ex:

        #NAME SECTION
        ex.write("{:<14}".format('NAME'))
        ex.write('Example')

        #ROWS SECTION
        ex.write("\nROWS\n")
        for type, name in zip(constType, constName):
            ex.write("{:>2}{:>4}".format(type, name))
            ex.write("\n")
        ex.write("{:>2}{:>4}".format('N', 'OBJ'))
        ex.write("\n")

        #COLUMNS SECTION
        ex.write("COLUMNS\n")

        for i in range(len(varName)):

            ex.write("{:>6}".format(varName[i]))
            for name, coef in zip(constName, A[i]):
                ex.write("{:>10}{:>20}".format(name,coef))
                ex.write("\n")
                ex.write("{:>6}".format(varName[i]))
            ex.write("{:>11}{:>19}".format('OBJ',c[i]))
            ex.write("\n")

        #RHS SECTION
        ex.write("RHS\n")
        for name, value in zip(constName, b):
            ex.write("{:>5}{:>11}{:>20}".format('R', name, value))
            ex.write("\n")

        ex.write("\nENDATA\n")


#--- MAIN ---

print("Convert a text file to an mps file format")
txFilename = input("Give the name of the text file you want to convert: ")
mpFilename = input("Give the name of MPS file with .mps extension: ")

with open(txFilename, 'r') as lp:

    line = lp.readline()
    arr = [] #the elements of this array are the lines of text file as strings
    while (line[:1] != 'b'):
        elemArr = line[1:].strip()

        if elemArr != '':
            elemArr = elemArr.lstrip("=[")
            elemArr = elemArr.strip("]")
            elemArr = elemArr.replace('\t', ' ')
            arr.append(elemArr)
        line = lp.readline()

    stArr = [] # a list of lists with elements each number of the line as STRING
    for i in range(len(arr)):
        num = arr[i].split()
        stArr.append(num)

    stArr = [[float(string) for string in lists] for lists in stArr] # a list of lists with elements each number of the line as FLOAT

    npArr = np.array(stArr)
    trArr = np.transpose(npArr)
    trList = trArr.tolist()

    # RIGHT VALUES OF CONSTRAINTS
    rightVal = []
    while (line[:1] != 'c'):

        value = line[3:].rstrip()
        if value != '':
            value = value.strip("]")
            rightVal.append(value)
        line = lp.readline()
    rightVal = [float(num) for num in rightVal ]

    # COEFFICIENTS OF VARIABLES IN OBJECTIVE FUNCTION
    coefObj = []

    while (line[:4] != 'Eqin'):

        coef = line[3:].rstrip()
        if coef != '':
            coef = coef.strip("]")
            coefObj.append(coef)
        line = lp.readline()

    coefObj = [float(num) for num in coefObj ]

    # LIST OF THE NAME OF VARIABLES
    nameVar = []
    for i in range(len(coefObj)):
        nameVar.append("X" + str(i))

    # TYPE OF CONSTRAINTS
    typeConst = []

    while(line[:6] != 'MinMax'):
        type = line[3:].rstrip()

        if type != '':
            type = type.lstrip("n=[")
            type = type.strip("]")
            if (type == '-1'):
                typeConst.append('L')
            elif (type == '1' ):
                typeConst.append('G')
            else:
                typeConst.append('E')
        line = lp.readline()

    # LIST OF THE LABELS OF CONSTRAINTS
    nameConst = []
    for i in range(len(typeConst)):
        nameConst.append("C" + str(i))

writeMps(mpFilename, trList, rightVal, coefObj, nameVar, typeConst, nameConst)
