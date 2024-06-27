import csv
import datetime
import os

ORIGINAL_PATH = ''
FINAL_PATH=''

ORIGINAL_FIELDNAMES = []
FINAL_FIELDNAMES = []

ORIGINAL_UNMATCHED_FIELDNAMES = []
FINAL_UNMATCHED_FIELDNAMES = []
COMPARISON_FIELDNAMES = []

ORIGINAL_ROW_ID = []
FINAL_ROW_ID = []

ORIGINAL_UNMATCHED_ROW_ID = []
FINAL_UNMATCHED_ROW_ID = []
COMPARISON_ROW_ID = []

ORIGINAL_DATA = {}
FINAL_DATA = {}

RESULTS_PATH='Results'

testlist1 = [1,2,3,4,'E',5,'l','l']
testlist2 = [1,'W',2,3,4,'K',5,'s','s']

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

def separate_duplicate_values(list, type):
    print('Analysing duplicate '+type)
    duplicates =[]
    unique=[]
    for value in list:
        if list.count(value)>1:
            if duplicates.count(value)==0:
                duplicates.append(value)
        else:
            unique.append(value)
    print('Finished analysing duplicate '+type)
    return {'duplicates':duplicates, 'unique':unique}

def separate_unmatched_values(original, final, type):
    print('Analysing unmatched '+type)
    matched = []
    original_unmatched = []
    final_unmatched = final[:]

    for name in original:
        if final.count(name)==0:
            original_unmatched.append(name)
        elif final.count(name)>1:    
            final_unmatched.pop(final_unmatched.index(name))
        else:
            final_unmatched.pop(final_unmatched.index(name))    
            matched.append(name)
    print('Finished analysing unmatched '+type)
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
    with open(results_path+'/'+title+'.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for value in list:
            csv_writer.writerow([value])
    print('Created '+title+' result csv')

def comparison_writer(original_data,final_data,comparison_fieldnames,comparison_row_id,results_path):
    print('Comparing Data')
    result_fieldnames=comparison_fieldnames[:]
    result_fieldnames.insert(0,'Sheet Comparison Row ID')
    with open(results_path+'/'+'Sheet Comparison.csv', 'w') as csvfile:
        csv_writer = csv.DictWriter(csvfile,fieldnames=result_fieldnames)
        csv_writer.writeheader()
        for id in comparison_row_id:
            compared_row = row_comparison(id,original_data[id],final_data,comparison_fieldnames)
            if compared_row['differences']:
                csv_writer.writerow(compared_row['row_object'])
    print('Finished Comparing Data')

def row_comparison(id,row,final_data,comparison_fieldnames):
    result={'differences':False, 'row_object':{}}
    result['row_object']['Sheet Comparison Row ID']=id
    for name in comparison_fieldnames:
        original_value=row[name]
        final_value=final_data[id][name]
        if original_value==final_value:
            result['row_object'][name]=''
        else:
            result['differences']=True
            result['row_object'][name]=original_value+' || '+final_value
    return result



# ORIGINAL_FIELDNAMES = read_fieldnames('original.csv')
# FINAL_FIELDNAMES = read_fieldnames('final.csv')

# ORIGINAL_ROW_ID=read_row_id('original.csv','id')
# FINAL_ROW_ID=read_row_id('final.csv','id')

# ORIGINAL_DATA=parse_data('original.csv')
# FINAL_DATA=parse_data('final.csv')

# unmatched_fieldname_results=separate_unmatched_values(ORIGINAL_FIELDNAMES,FINAL_FIELDNAMES,'fieldnames')
# ORIGINAL_UNMATCHED_FIELDNAMES=unmatched_fieldname_results['original_unmatched']
# FINAL_UNMATCHED_FIELDNAMES=unmatched_fieldname_results['final_unmatched']
# COMPARISON_FIELDNAMES=unmatched_fieldname_results['comparison']

# write_list_csv("Original Unmatched Fieldnames", ORIGINAL_UNMATCHED_FIELDNAMES, RESULTS_PATH)
# write_list_csv("Final Unmatched Fieldnames", FINAL_UNMATCHED_FIELDNAMES, RESULTS_PATH)

# unmatched_row_id_results=separate_unmatched_values(ORIGINAL_ROW_ID,FINAL_ROW_ID,'row ID')
# ORIGINAL_UNMATCHED_ROW_ID=unmatched_row_id_results['original_unmatched']
# FINAL_UNMATCHED_ROW_ID=unmatched_row_id_results['final_unmatched']
# COMPARISON_ROW_ID=unmatched_row_id_results['comparison']

# write_list_csv("Original Unmatched Row ID", ORIGINAL_UNMATCHED_ROW_ID, RESULTS_PATH)
# write_list_csv("Final Unmatched Row ID", FINAL_UNMATCHED_ROW_ID, RESULTS_PATH)

# comparison_writer(ORIGINAL_DATA,FINAL_DATA,COMPARISON_FIELDNAMES,COMPARISON_ROW_ID,RESULTS_PATH)

print(separate_duplicate_values(testlist2,'fieldnames'))