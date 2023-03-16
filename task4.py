import random
import time
import xlsxwriter
import json

# --- Quick sort / middle version ---
def partitionQS(tab, p, r):
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

def sortQS(tab, p, r):
  if p < r:
    sub_tab = partitionQS(tab, p, r)
    sortQS(tab, p, sub_tab)
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


# - DATA PART
# - GENERATE RANGES -
startNumber = 5000
n = 15
dataRange = [x for x in range(startNumber, startNumber + (n - 1) * 1000 + 1, 1000)]

# - TEMPLATE -
templateA = [
    {
        "name": "elements",
        "data": []
    },
    {
        "name": "time CS",
        "data": []
    },
    {
        "name": "time QS",
        "data": []
    }
]

templateB = [
    {
        "name": "elements",
        "data": []
    },
    {
        "name": "time CS",
        "data": []
    },
    {
        "name": "time QS",
        "data": []
    }
]

# - GENERATE DATA FOR [1, 100n] -
for r in dataRange:
    data = [random.randint(1, 100*r) for i in range(r)]
    templateA[0]["data"].append(r)

    #CS
    testForCS = data.copy()
    startCS = time.time()
    sortCS(testForCS)
    resultCS = time.time() - startCS
    templateA[1]["data"].append(resultCS)

    #QS
    testForQS = data.copy()
    startQS = time.time()
    sortQS(testForQS, 0, len(testForQS) - 1)
    resultQS = time.time() - startQS
    templateA[2]["data"].append(resultQS)


# - GENERATE DATA FOR [1, 0.01n] -
for r in dataRange:
    data = [random.randint(1, r//100) for i in range(r)]
    templateB[0]["data"].append(r)

    #CS
    testForCS = data.copy()
    startCS = time.time()
    sortCS(testForCS)
    resultCS = time.time() - startCS
    templateB[1]["data"].append(resultCS)

    #QS
    testForQS = data.copy()
    startQS = time.time()
    sortQS(testForQS, 0, len(testForQS) - 1)
    resultQS = time.time() - startQS
    templateB[2]["data"].append(resultQS)


# - JSON DATA -
with open("task4-resultsA.json", "w", encoding="utf-8") as file:
    json.dump(templateA, file, indent=2)
with open("task4-resultsB.json", "w", encoding="utf-8") as file:
    json.dump(templateB, file, indent=2)

# - DATA TO EXCEL FILE -
workbook = xlsxwriter.Workbook("task4-excel.xlsx")
worksheet = workbook.add_worksheet("main")

worksheet.write(0, 0, "point a")
for idx, t in enumerate(templateA):
    worksheet.write(1, idx, t["name"])
    for i in range(len(t["data"])):
        worksheet.write(i + 2, idx, t["data"][i])

worksheet.write(0, 5, "point b")
for idx, t in enumerate(templateB):
    worksheet.write(1, idx+5, t["name"])
    for i in range(len(t["data"])):
        worksheet.write(i + 2, idx+5, t["data"][i])

workbook.close()
