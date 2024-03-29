import numpy as np 

def main():  
    with open('file.mps', 'r') as f:
        m = 0  #dimension m - number of constraints, doesn't include obj
        const = {}
        line = f.readline()  # first line with NAME
        if line[:4] == 'NAME':
            print("The name of the MPS file is", line[14:].strip(), ".")
            print(" ")

        # >>>>> START :   BUILD CONSTRAINTS

        line = f.readline()  # second line with ROWS

        line = f.readline()
        while (line[:7] != 'COLUMNS'):

            if (line[1:2] != 'N'):
                m += 1

            typeConst = line[1:2].strip()
            if typeConst in ['E', 'L', 'G']:
                labels = line[4:].strip()
                const[labels] = typeConst

            if typeConst == 'N':
                obj = []

            line = f.readline()

            eqin = []
            constVal = list(const.values())
            for i in constVal:
                if (i == 'E'):
                    eqin.append(0)
                elif (i == 'L'):
                    eqin.append(-1)
                else:
                    eqin.append(1)

        # <<<<<<<<<   END  BUILD CONSTRAINS

        listLbl = list(const.keys())

        #>>>>>>>>>>>>>>>>>>>>> START: COLUMNS SECTION

        firstCol = []
        var = []
        setVar = set()

        line = f.readline()
        while (line[:3] != 'RHS'):

            lbl = line[4:14].strip()  # X01, X01, X02, X02, X03, X04,...

            if lbl not in setVar:
                setVar.add(lbl)
                var.append(lbl)  # X01, X02, X03, X04,..

                lenVar = len(var)
                lblIdx = var.index(lbl)

                var[lblIdx] = {}

            varDict = var[lblIdx]

            key1 = line[14:23].strip()
            key2 = line[39:48].strip()


            if key1 in listLbl:
                varDict[key1] = line[24:37].strip()

            if key2 in listLbl:
                varDict[key2] = line[49:].strip()

            for key in listLbl:
                if key not in varDict.keys():
                    varDict[key] = 0


            if key1 not in listLbl:
                obj.insert(lblIdx, line[24:37].strip())

            elif key2 not in listLbl and len(key2) != 0:
                obj.insert(lblIdx, line[49:].strip())
            else:
                obj.insert(lblIdx, 0)


            lenObj = len(obj)
            if (lenObj > lenVar):
                for i in range(lenVar, lenObj):
                    obj.remove(0)

            line = f.readline()  # reaches RHS and stops


        coeff = []
        for d in var:
            for key in listLbl:
                coeff.append(d[key])


        # COEFFICIENTS OF OBJECTIVE FUNCTION
        fObj = [float(x) for x in obj ]

        #  COEFFICIENTS OF VARIABLES OF THE CONSTRAINTS
        A = np.array(coeff)
        A = A.reshape((lenVar, m ))

        #<<<<<<<<<<<<<<<<<<<<<<<<<< END: COLUMNS SECTION


        #>>>>>>>>>>>>>>>>>>>>>>>>>> START: RHS SECTION
        rightVal = {}

        line = f.readline()
        while (line[:6] != 'ENDATA'):
            key14 = line[14:23].strip()
            key39 = line[39:48].strip()

            if len(key14) > 0:
                if key14 in listLbl:
                    rightVal[key14] = line[24:37].strip()
                else:
                    rightVal[key14] = 0

            if len(key39) > 0:
                if key39 in listLbl:
                    rightVal[key39] = line[49:].strip()
                else:
                    rightVal[key39] = 0

            for key in listLbl:
                if key not in rightVal.keys():
                    rightVal[key] = 0

            b = list(rightVal.values())
            fb = [ float(x) for x in b ]

            line = f.readline()

        #<<<<<<<<<<<<<<<<<<<<<<<<<< END: RHS SECTION

    rowA = np.transpose(A) #A is by column -> transpose -> by row
    floatA = rowA.astype(float)
    print(floatA.shape[0], floatA.shape[1])
    print("A = ", floatA, "\n")
    eqin = np.array(eqin)
    print(eqin.shape)
    print("Eqin = ", eqin, "\n")
    b = np.array(fb)
    print(b.shape)
    print("b = ", b, "\n")
    c = np.array(fObj)
    print(c.shape)
    print("c = ", c, "\n")
    
if __name__=="__main__":
  main()