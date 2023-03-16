import random
import time
import xlsxwriter
import json

# --- EXTREME Iterative Quick sort --- (used - own stack)
def partitionQS_exti(tab, p, r):
    i = (p - 1)
    pivot = tab[r]

    for j in range(p, r):
        if tab[j] <= pivot:
            i = i + 1
            tab[i], tab[j] = tab[j], tab[i]

    tab[i + 1], tab[r] = tab[r], tab[i + 1]
    return i + 1

def sortQS_exti(tab, p, r):
    #stack
    size = r - p + 1
    stack = [0] * (size)
    top = 0
    stack[top] = p
    top = top + 1
    stack[top] = r

    while top >= 0:
        r = stack[top]
        top = top - 1
        p = stack[top]
        top = top - 1

        sub_tab = partitionQS_exti(tab, p, r)

        if sub_tab - 1 > p:
            top = top + 1
            stack[top] = p
            top = top + 1
            stack[top] = sub_tab - 1

        if sub_tab + 1 < r:
            top = top + 1
            stack[top] = sub_tab + 1
            top = top + 1
            stack[top] = r


# --- EXTREME Quick sort --- (not used - stack overflow)
def partitionQS_ext(tab, p, r):
    pivot = tab[r]
    i = p - 1
    for j in range(p, r):
        if tab[j] <= pivot:
            i = i + 1
            (tab[i], tab[j]) = (tab[j], tab[i])
    (tab[i + 1], tab[r]) = (tab[r], tab[i + 1])

    return i + 1

def sortQS_ext(tab, p, r):
    if p < r:
        sub_tab = partitionQS_ext(tab, p, r)
        sortQS_ext(tab, p, sub_tab - 1)
        sortQS_ext(tab, sub_tab + 1, r)


# --- MIDDLE Quick sort ---
def partitionQS_mid(tab, p, r):
  pivot = tab[(p + r) // 2]
  i = p - 1
  j = r + 1
  while True:
    i += 1
    while tab[i] < pivot:
      i += 1
    j -= 1
    while tab[j] > pivot:
      j -= 1
    if i >= j:
      return j
    tab[i], tab[j] = tab[j], tab[i]

def sortQS_mid(tab, p, r):
  if p < r:
    sub_tab = partitionQS_mid(tab, p, r)
    sortQS_mid(tab, p, sub_tab)
    sortQS_mid(tab, sub_tab + 1, r)


# --- Insertion sort ---
def sortIS(tab):
  for i in range(1, len(tab)):
    key = tab[i]
    j = i - 1
    while j >= 0 and tab[j] > key:
      tab[j + 1] = tab[j]
      j -= 1

    tab[j + 1] = key


# --- DATA PART ---
# - GENERATE RANGES -
startNumber = 2000
n = 15
dataRange = [x for x in range(startNumber, startNumber + (n - 1) * 1000 + 1, 1000)]

# - TEMPLATE -
tempRandom = [
    {
        "name": "elements",
        "data": []
    },
    {
        "name": "time QS_ext",
        "data": []
    },
    {
        "name": "time QS_mid",
        "data": []
    },
    {
        "name": "time IS",
        "data": []
    }
]

tempIncreasing = [
    {
        "name": "elements",
        "data": []
    },
    {
        "name": "time QS_ext",
        "data": []
    },
    {
        "name": "time QS_mid",
        "data": []
    },
    {
        "name": "time IS",
        "data": []
    }
]

# - GENERATE DATA -
for r in dataRange:
    data = [random.randint(1, r) for i in range(r)]
    tempRandom[0]["data"].append(r)
    tempIncreasing[0]["data"].append(r)

    #Extreme QS
    testForQS_ext = data.copy()
    startQS_ext = time.time()
    sortQS_ext(testForQS_ext, 0, len(testForQS_ext) - 1)
    resultQS_ext = time.time() - startQS_ext
    tempRandom[1]["data"].append(resultQS_ext)

    startQS_ext = time.time()
    sortQS_exti(testForQS_ext, 0, len(testForQS_ext) - 1)
    resultQS_ext = time.time() - startQS_ext
    tempIncreasing[1]["data"].append(resultQS_ext)

    #Middle QS
    testForQS_mid = data.copy()
    startQS_mid = time.time()
    sortQS_mid(testForQS_mid, 0, len(testForQS_mid) - 1)
    resultQS_mid = time.time() - startQS_mid
    tempRandom[2]["data"].append(resultQS_mid)

    startQS_mid = time.time()
    sortQS_mid(testForQS_mid, 0, len(testForQS_mid) - 1)
    resultQS_mid = time.time() - startQS_mid
    tempIncreasing[2]["data"].append(resultQS_mid)

    #IS
    testForIS = data.copy()
    startIS = time.time()
    sortIS(testForIS)
    resultIS = time.time() - startIS
    tempRandom[3]["data"].append(resultIS)

    startIS = time.time()
    sortIS(testForIS)
    resultIS = time.time() - startIS
    tempIncreasing[3]["data"].append(resultIS)


# - JSON DATA -
with open("task3-resultsRandom.json", "w", encoding="utf-8") as file:
    json.dump(tempRandom, file, indent=2)
with open("task3-resultsIncreasing.json", "w", encoding="utf-8") as file:
    json.dump(tempIncreasing, file, indent=2)

# - DATA TO EXCEL FILE -
workbook = xlsxwriter.Workbook("task3-excel.xlsx")
worksheet = workbook.add_worksheet("main")

worksheet.write(0, 0, "random")
for idx, t in enumerate(tempRandom):
    worksheet.write(1, idx, t["name"])
    for i in range(len(t["data"])):
        worksheet.write(i + 2, idx, t["data"][i])

worksheet.write(0, 5, "increasing")
for idx, t in enumerate(tempIncreasing):
    worksheet.write(1, idx+5, t["name"])
    for i in range(len(t["data"])):
        worksheet.write(i + 2, idx+5, t["data"][i])

workbook.close()
