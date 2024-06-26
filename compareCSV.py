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
    print('Reading '+file_path+' fieldnames')
    fieldnames=[]
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            fieldnames=row
            break
    print('Finished reading '+file_path+' fieldnames')
    return fieldnames

def read_row_id(file_path, id_fieldname):
    print('Reading '+file_path+' row IDs')
    id_list=[]
    with open(file_path, 'r') as csvdictfile:
        dict_csv_reader = csv.DictReader(csvdictfile)
        for row in dict_csv_reader:
            id_list.append(row[id_fieldname])
    print('Finished reading '+file_path+' row IDs')
    return id_list

def parse_data(file_path):
    print('Parsing '+file_path+' data')
    data_dict={}
    with open(file_path, 'r') as csvdictfile:
        dict_csv_reader = csv.DictReader(csvdictfile)
        for row in dict_csv_reader:
            data_dict[row['id']]=row
    print('Finished parsing '+file_path+' data')
    return data_dict

def seperate_unmatched_fieldnames(original, final):
    print('Analysing unmatched fieldnames')
    matched = []
    final_unmatched = final[:]
    original_unmatched = []
    for name in original:
        if final.count(name)>0:
            final_unmatched.pop(final_unmatched.index(name))
            matched.append(name)
        else:
            original_unmatched.append(name)
    print('Finished analysing unmatched fieldnames')
    return {
            'original_unmatched':original_unmatched,
            'final_unmatched':final_unmatched,
            'comparison': matched
            }

def create_results_folder():
    result_path = 'Results - '+str(datetime.datetime.today())[0:19]
    os.makedirs(result_path)
    print("Results folder created")
    return result_path

def write_list_csv(title,list,results_path):
    print('Creating '+title+' result csv')
    list.insert(0,title)
    with open(results_path+'/'+title, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for value in list:
            csv_writer.writerow([value])
    print('Created '+title+' result csv')


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

write_list_csv("Original Unmatched Fieldnames", ORIGINAL_UNMATCHED_FIELDNAMES, RESULTS_PATH)
write_list_csv("Final Unmatched Fieldnames", FINAL_UNMATCHED_FIELDNAMES, RESULTS_PATH)