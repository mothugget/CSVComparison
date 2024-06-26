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

def read_fieldnames(file_path):
    fieldnames=[]
    with open(file_path, 'r') as csvfile:
        original_csv_reader = csv.reader(csvfile)
        for row in original_csv_reader:
            fieldnames=row
            break
    return fieldnames

def read_id(file_path, id_fieldname):
    id_list=[]
    with open(file_path, 'r') as csvfile:
        original_csv_reader = csv.reader(csvfile)
        for row in original_csv_reader:
            id_list.append(row[id_fieldname])
    return id_list

def parse_data(file_path):
    data_dict={}
    with open(file_path, 'r') as csvdictfile:
        original_dict_csv_reader = csv.DictReader(csvdictfile)
        for row in original_dict_csv_reader:
            data_dict[row['id']]=row
    return data_dict

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
    print("original ",original_unmatched," final ",final_unmatched,' matched ', matched)

seperate_unmatched_fieldnames(testlist1,testlist2)
