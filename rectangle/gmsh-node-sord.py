
allList = []
with open("./rectangle.msh", "r") as f:
    # for i, line in enumerate(f):
    #     if line == "$MeshFormat\n":
    #         print("test")
    #         # exit()
    #     lineSplit = line.split(' ')
    #     print(i, lineSplit[0])
    #     i += 1
    allList = f.read().split("\n")

# print(allList)


counter = 0
intPhysicalNames = 0
intNodes = 0
intElements = 0
listPhysicalNames = []
listNodes = []
listElements = []
indexOrigin = []
indexChange = []
correspondence = []
print(len(allList))
for i in range(len(allList)):
    # print(i, allList[i])
    # print(i + counter)
    counter = 0
    if len(allList) < i + counter:
        break
    elif allList[i + counter] == "$MeshFormat":
        # print(i, allList[i])
        print(i, "test")
        counter += 2
    elif allList[i + counter] == "$PhysicalNames":
        # print(i + counter)
        counter += 1
        intPhysicalNames = int(allList[i + counter])
        counter += 1
        for j in range(intPhysicalNames):
            test = allList[i + counter + j].split(' ')
            listPhysicalNamesTemp = [test[0], test[1], test[2]]
            listPhysicalNames.append(listPhysicalNamesTemp)
        # print(i + counter, allList[i + counter])
    elif allList[i + counter] == "$Nodes":
        print(i, "nodes")
        counter += 1
        intNodes = int(allList[i + counter])
        counter += 1
        for j in range(intNodes):
            test = allList[i + counter + j].split(' ')
            print(f"{test[0]}, {test[1]}, {test[2]}, {test[3]}")
            listNodesTemp = [(test[1]), (test[2]), (test[3])]
            listNodes.append(listNodesTemp)
    elif allList[i] == "$Elements":
        print(i, "Elements")
        counter += 1
        intElements = int(allList[i + counter])
        counter += 1
        for j in range(intElements):
            print(i + counter + j)
            test = allList[i + counter + j].split(' ')
            if test[1] == "1":
                listElementsTemp = [test[0], test[1], test[2], test[3], test[4], test[5], test[6]]
                print(f"line {test[0]}")
            elif test[1] == "2":
                listElementsTemp = [test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7]]
                print(f"triangle {test[0]}")
            elif test[1] == "3":
                listElementsTemp = [test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7], test[8]]
                print(f"quadrangle {test[0]}")
            listElements.append(listElementsTemp)
    # counter += 1


# for i, line in enumerate(allList):
#     print(i, line)



print(f"intPhysicalNames = {intPhysicalNames}")
print(f"intNodes = {intNodes}")
print(f"intElements = {intElements}")


for i, node in enumerate(listNodes):
    indexOrigin.append(node[0] + node[1] + node[2])
    # print(f"{i}, {node}")

listNodesSorted = sorted(listNodes , key=lambda k: [k[0], k[1], k[2]])
for i, node in enumerate(listNodesSorted):
    indexChange.append(node[0] + node[1] + node[2])
    # print(f"{i}, {node}")

# for i, iC in enumerate(indexChange):
#     print(f"{i}, {indexOrigin.index(iC)}")

# correspondence.append("-1")
for i, iO in enumerate(indexOrigin):
    correspondence.append(indexChange.index(iO))
    # print(f"{i}, {indexChange.index(iO)}")

# print("------------")

for i in range(len(correspondence)):
    print(f"{i} {correspondence[i]}")
print(len(correspondence))
# exit()
# for i, t in enumerate(correspondence):
    # print(f"{i} {t}")


# exit()

# for i, lp in enumerate(listPhysicalNames):
#     print(f"{i}, {lp}")

# for i, lN in enumerate(listNodesSorted):
#     print(f"{i} {lN}")

# for i, el in enumerate(listElements):
#     print(f"{i}, {el}")


with open("./rectangle-sort.msh", "w", encoding='utf-8', newline='\n') as f:
    f.writelines("$MeshFormat\n")
    f.writelines("2.2 0 8\n")
    f.writelines("$EndMeshFormat\n")
    f.writelines("$PhysicalNames\n")
    f.writelines(f"{intPhysicalNames}\n")
    for lP in listPhysicalNames:
        f.writelines(f"{lP[0]} {lP[1]} {lP[2]}\n")
    f.writelines("$EndPhysicalNames\n")
    f.writelines("$Nodes\n")
    f.writelines(f"{intNodes}\n")
    for i, lN in enumerate(listNodesSorted):
        f.writelines(f"{i + 1} {lN[0]} {lN[1]} {lN[2]}\n")
    f.writelines("$EndNodes\n")
    f.writelines("$Elements\n")
    f.writelines(f"{intElements}\n")
    for i, lE in enumerate(listElements):
        print(i + 1)
        one = str(correspondence[int(lE[4]) - 1] + 1)
        two = str(correspondence[int(lE[5]) - 1] + 1)
        three = str(correspondence[int(lE[6]) - 1] + 1)
        if lE[1] == "1":
            f.writelines(f"{lE[0]} {lE[1]} {lE[2]} {lE[3]} {one} {two} {three}\n")
        elif lE[1] == "2":
            four = str(correspondence[int(lE[7]) - 1] + 1)
            f.writelines(f"{lE[0]} {lE[1]} {lE[2]} {lE[3]} {one} {two} {three} {four}\n")
        elif lE[1] == "3":
            four = str(correspondence[int(lE[7]) - 1] + 1)
            five = str(correspondence[int(lE[8]) - 1] + 1)
            f.writelines(f"{lE[0]} {lE[1]} {lE[2]} {lE[3]} {one} {two} {three} {four} {five}\n")
            print("test")
    f.writelines("$EndElements")
    print("EndElements")





