import csv
import datetime
import os

ORIGINAL_FIELDNAMES = []
FINAL_FIELDNAMES = []

ORIGINAL_UNMATCHED_FIELDNAMES = []
FINAL_UNMATCHED_FIELDNAMES = []
COMPARISON_FIELDNAMES = []

ORIGINAL_ROW_ID = []
FINAL_ROW_ID = []

ORIGINAL_DATA = {}
FINAL_DATA = {}

RESULTS_PATH='Results'

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

def read_row_id(file_path, id_fieldname):
    id_list=[]
    with open(file_path, 'r') as csvdictfile:
        original_dict_csv_reader = csv.DictReader(csvdictfile)
        for row in original_dict_csv_reader:
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
    matched = []
    final_unmatched = final[:]
    original_unmatched = []
    for name in original:
        if final.count(name)>0:
            final_unmatched.pop(final_unmatched.index(name))
            matched.append(name)
        else:
            original_unmatched.append(name)
    return {
            'original_unmatched':original_unmatched,
            'final_unmatched':final_unmatched,
            'comparison': matched
            }

ORIGINAL_FIELDNAMES = read_fieldnames('original.csv')
FINAL_FIELDNAMES = read_fieldnames('final.csv')

ORIGINAL_ROW_ID=read_row_id('original.csv','id')
FINAL_ROW_ID=read_row_id('final.csv','id')

ORIGINAL_DATA=parse_data('original.csv')
FINAL_DATA=parse_data('final.csv')

unmatched_results=seperate_unmatched_fieldnames(ORIGINAL_FIELDNAMES,FINAL_FIELDNAMES)
ORIGINAL_UNMATCHED_FIELDNAMES=unmatched_results['original_unmatched']
FINAL_UNMATCHED_FIELDNAMES=unmatched_results['final_unmatched']
COMPARISON_FIELDNAMES=unmatched_results['comparison']

# print(ORIGINAL_UNMATCHED_FIELDNAMES)
# print(FINAL_UNMATCHED_FIELDNAMES)
# print(COMPARISON_FIELDNAMES)

# a = [1, 2, 3, 4]
# b = [x*x for x in a]
# print(a,"\n",b )

def create_results_folder():
    result_path = 'Results - '+str(datetime.datetime.today())[0:19]
    os.makedirs(result_path)
    print("Results folder created")
    return result_path

