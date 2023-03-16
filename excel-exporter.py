import json
import xlsxwriter

# JSON LOAD
fileName = input("Give a filename for json results to export to Excel: ")

with open(f'{fileName}.json', 'r', encoding="utf-8") as file:
    data = json.load(file)
    print("Data loaded succesfully")

# - CREATING AND FILLING EXCEL FILE -
workbook = xlsxwriter.Workbook(f'{fileName}-excel.xlsx')
print(f'Creating {fileName}-excel.xlsx file...')
worksheet = workbook.add_worksheet("main")

for idx, t in enumerate(data):
    worksheet.write(0, idx, t["name"])
    for i in range(len(t["data"])):
        worksheet.write(i+1, idx, t["data"][i])

workbook.close()
print("Data has been exported to Excel")