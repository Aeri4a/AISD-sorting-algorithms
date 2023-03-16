import random
import time
import xlsxwriter
import json

# - SORTING FUCTIONS -

# --- Selection sort ---
def sortSS(tab):
    for i in range(len(tab)):
        minInd = i
        for j in range(i + 1, len(tab)):
            if tab[j] < tab[minInd]:
                minInd = j
        tab[i], tab[minInd] = tab[minInd], tab[i]


# --- Insertion sort ---
def sortIS(tab):
    for i in range(1, len(tab)):
        key = tab[i]
        j = i - 1
        while j >= 0 and tab[j] > key:
            tab[j + 1] = tab[j]
            j -= 1

        tab[j + 1] = key


# --- Bubble sort ---
def sortBS(tab):
    swapped = True

    while swapped:
        swapped = False

        for i in range(len(tab) - 1):
            if tab[i] > tab[i + 1]:
                tab[i], tab[i + 1] = tab[i + 1], tab[i]
                swapped = True


# --- Heap sort ---
def heapifyHS(tab, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and tab[i] < tab[l]:
        largest = l

    if r < n and tab[largest] < tab[r]:
        largest = r

    if largest != i:
        tab[i], tab[largest] = tab[largest], tab[i]
        heapifyHS(tab, n, largest)

def sortHS(tab):
    n = len(tab)

    for i in range(n // 2, -1, -1):
        heapifyHS(tab, n, i)

    for i in range(n - 1, 0, -1):
        tab[i], tab[0] = tab[0], tab[i]

        heapifyHS(tab, i, 0)


# --- Merge sort ---
def sortMS(tab):
    if len(tab) > 1:
        point = len(tab) // 2
        left_tab = tab[:point]
        right_tab = tab[point:]

        sortMS(left_tab)
        sortMS(right_tab)

        i = j = k = 0

        while i < len(left_tab) and j < len(right_tab):
            if left_tab[i] <= right_tab[j]:
                tab[k] = left_tab[i]
                i += 1
            else:
                tab[k] = right_tab[j]
                j += 1
            k += 1

        while i < len(left_tab):
            tab[k] = left_tab[i]
            i += 1
            k += 1

        while j < len(right_tab):
            tab[k] = right_tab[j]
            j += 1
            k += 1


# --- Quick sort ---
def partitionQS(tab, p, r):
    pivot = tab[r]
    i = p - 1
    for j in range(p, r):
        if tab[j] <= pivot:
            i = i + 1
            (tab[i], tab[j]) = (tab[j], tab[i])
    (tab[i + 1], tab[r]) = (tab[r], tab[i + 1])

    return i + 1

def sortQS(tab, p, r):
    if p < r:
        sub_tab = partitionQS(tab, p, r)
        sortQS(tab, p, sub_tab - 1)
        sortQS(tab, sub_tab + 1, r)


# --- Counting sort ---
def sortCS(tab):
    size = len(tab)
    output = [0] * size

    count = [0] * (max(tab) + 1)

    for i in range(0, size):
        count[tab[i]] += 1

    for i in range(1, max(tab) + 1):
        count[i] += count[i - 1]

    i = size - 1
    while i >= 0:
        output[count[tab[i]] - 1] = tab[i]
        count[tab[i]] -= 1
        i -= 1

    for i in range(0, size):
        tab[i] = output[i]


# --- DATA PART ---
# - GENERATE RANGES -
startNumber = 2000
n = 15
dataRange = [x for x in range(startNumber, startNumber + (n - 1) * 1000 + 1, 1000)] # [1000,1500...]

# - TEMPLATE -
tempData = [
    {
        "name": "elements",
        "data": []
    },
    {
        "name": "time SS",
        "data": []
    },
    {
        "name": "time IS",
        "data": []
    },
    {
        "name": "time BS",
        "data": []
    },
    {
        "name": "time HS",
        "data": []
    },
    {
        "name": "time MS",
        "data": []
    },
    {
        "name": "time QS",
        "data": []
    },
    {
        "name": "time CS",
        "data": []
    }
]

# - GENERATE DATA -
for r in dataRange:
    data = [random.randint(1, r) for i in range(r)]
    tempData[0]["data"].append(r)

    #Selection Sort
    testForSS = data.copy()
    startSS = time.time()
    sortSS(testForSS)
    resultSS = time.time() - startSS
    tempData[1]["data"].append(resultSS)

    #Insertion Sort
    testForIS = data.copy()
    startIS = time.time()
    sortIS(testForIS)
    resultIS = time.time() - startIS
    tempData[2]["data"].append(resultIS)

    #Bubble Sort
    testForBS = data.copy()
    startBS = time.time()
    sortBS(testForBS)
    resultBS = time.time() - startBS
    tempData[3]["data"].append(resultBS)

    #Heap Sort
    testForHS = data.copy()
    startHS = time.time()
    sortHS(testForHS)
    resultHS = time.time() - startHS
    tempData[4]["data"].append(resultHS)

    #Merge Sort
    testForMS = data.copy()
    startMS = time.time()
    sortMS(testForMS)
    resultMS = time.time() - startMS
    tempData[5]["data"].append(resultMS)

    #Quick Sort
    testForQS = data.copy()
    startQS = time.time()
    sortQS(testForQS, 0, len(testForQS)-1)
    resultQS = time.time() - startQS
    tempData[6]["data"].append(resultQS)

    #Counting Sort
    testForCS = data.copy()
    startCS = time.time()
    sortCS(testForCS)
    resultCS = time.time() - startCS
    tempData[7]["data"].append(resultCS)


# - JSON DATA -
with open("task12-results.json", "w", encoding="utf-8") as file:
    json.dump(tempData, file, indent=2)

# - DATA TO EXCEL FILE -
workbook = xlsxwriter.Workbook("task12-excel.xlsx")
worksheet = workbook.add_worksheet("main")

for idx, t in enumerate(tempData):
    worksheet.write(0, idx, t["name"])
    for i in range(len(t["data"])):
        worksheet.write(i+1, idx, t["data"][i])

workbook.close()