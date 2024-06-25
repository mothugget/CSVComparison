import csv

ORIGINAL_FIELDNAMES = []
FINAL_FIELDNAMES = []

ORIGINAL_UNMATCHED_FIELDNAMES = []
FINAL_UNMATCHED_FIELDNAMES = []
COMPARISON_FIELDNAMES = []

ORIGINAL_DATA = {}
FINAL_DATA = {}

testlist1 = [1,2,3,4,'E',5]
testlist2 = [1,'W',2,3,4,'K',5]


with open('original.csv', 'r') as csvfile:
    original_csv_reader = csv.reader(csvfile)
    for row in original_csv_reader:
        ORIGINAL_FIELDNAMES=row
        break

with open('original.csv', 'r') as csvdictfile:
    original_dict_csv_reader = csv.DictReader(csvdictfile)
    for row in original_dict_csv_reader:
        ORIGINAL_DATA[row['id']]=row

with open('final.csv', 'r') as csvfile:
    final_csv_reader = csv.reader(csvfile)
    for row in final_csv_reader:
        FINAL_FIELDNAMES=row
        break

with open('final.csv', 'r') as csvdictfile:
    final_dict_csv_reader = csv.DictReader(csvdictfile)
    for row in final_dict_csv_reader:
        FINAL_DATA[row['id']]=row

def seperate_unmatched_fieldnames(original, final):
    return_dict = {}
    matched = []
    final_unmatched = final[:]
    original_unmatched = []
    for name in original:
        if final.count(name)>0:
            final_unmatched.pop(final_unmatched.index(name))
            matched.append(name)
        else:
            original_unmatched.append(name)
    print(final)

seperate_unmatched_fieldnames(testlist1,testlist2)
