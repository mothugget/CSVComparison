import csv
import datetime
import os
print('Welcome to the CSV comparison script')
run_script:bool = True

while run_script == True:

    try:
        original_path,final_path,id_fieldname=eval(input("{'original_path': 'path1','final_path': 'path2',id_fieldname:'id'}\n"))
    except Exception as e:
        print(f'There seems to be an error \n{e}\n')
        continue_script=False
        try_again=True
        while try_again==True:
            try:
                run_script=eval(input('Would you like to try again? (True/False)'))
                try_again=False
            except Exception as e:
                print(f"Sorry, didn't quite catch that. Remember answers are case sensitive \n {e}\n")
    if continue_script:
        print(original_path)
        print(final_path)
    






def read_fieldnames(file_path):
    print('Reading ' + file_path + ' fieldnames')
    fieldnames = []
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            fieldnames = row
            break
    print('Finished reading ' + file_path + ' fieldnames')
    return fieldnames

def read_row_id(file_path, id_fieldname):
    print('Reading ' + file_path + ' row IDs')
    id_list = []
    with open(file_path, 'r') as csvdictfile:
        dict_csv_reader = csv.DictReader(csvdictfile)
        for row in dict_csv_reader:
            id_list.append(row[id_fieldname])
    print('Finished reading ' + file_path + ' row IDs')
    return id_list

def parse_data(file_path):
    print('Parsing ' + file_path + ' data')
    data_dict = {}
    with open(file_path, 'r') as csvdictfile:
        dict_csv_reader = csv.DictReader(csvdictfile)
        for row in dict_csv_reader:
            data_dict[row['id']] = row
    print('Finished parsing ' + file_path + ' data')
    return data_dict

def separate_duplicate_values(list, type):
    print('Analysing duplicate ' + type)
    duplicates = []
    unique = []
    for value in list:
        if list.count(value) > 1:
            if duplicates.count(value) == 0:
                duplicates.append(value)
        else:
            unique.append(value)
    print('Finished analysing duplicate ' + type)
    return {'duplicates': duplicates, 'unique': unique}

def separate_unmatched_values(original, final, original_duplicates, final_duplicates, type):
    print('Analysing unmatched ' + type)
    matched = []
    original_unmatched = []
    final_unmatched = final[:]

    for name in original:
        if final_duplicates.count(name) == 0:
            if final.count(name) == 0:
                original_unmatched.append(name)
            else:
                final_unmatched.remove(name)
                matched.append(name)

    final_unmatched = [name for name in final_unmatched if original_duplicates.count(name) == 0]

    print('Finished analysing unmatched ' + type)
    return {
        'original_unmatched': original_unmatched,
        'final_unmatched': final_unmatched,
        'comparison': matched
    }

def create_results_folder():
    result_path = 'Results - ' + str(datetime.datetime.today())[0:19]
    os.makedirs(result_path)
    print("Results folder created")
    return result_path

def write_list_csv(title, list, results_path):
    print('Creating ' + title + ' result csv')
    list.insert(0, title)
    with open(results_path + '/' + title + '.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for value in list:
            csv_writer.writerow([value])
    print('Created ' + title + ' result csv')

def comparison_writer(original_data, final_data, comparison_fieldnames, comparison_row_id, results_path):
    print('Comparing Data')
    result_fieldnames = comparison_fieldnames[:]
    result_fieldnames.insert(0, 'Sheet Comparison Row ID')
    with open(results_path + '/' + 'Sheet Comparison.csv', 'w') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames = result_fieldnames)
        csv_writer.writeheader()
        for id in comparison_row_id:
            compared_row = row_comparison(id, original_data, final_data, comparison_fieldnames)
            if compared_row['differences']:
                csv_writer.writerow(compared_row['row_object'])
    print('Finished Comparing Data')

def row_comparison(id, original_data, final_data, comparison_fieldnames):
    result = {'differences': False, 'row_object': {}}
    result['row_object']['Sheet Comparison Row ID'] = id
    for name in comparison_fieldnames:
        original_value = original_data[id][name]
        final_value = final_data[id][name]
        if original_value == final_value:
            result['row_object'][name] = ''
        else:
            result['differences'] = True
            result['row_object'][name] = original_value + ' || ' + final_value
    return result

def read_csv_data(original_path='', final_path='', id_fieldname=None):
    continue_script=True
    try:
        original_fieldnames = read_fieldnames(original_path)
        if id_fieldname==None:
            id_fieldname=original_fieldnames[0]
        final_fieldnames = read_fieldnames(final_path)
        original_row_id = read_row_id(original_path, id_fieldname)   
        final_row_id = read_row_id(final_path, id_fieldname)    
        original_data = parse_data(original_path)    
        final_data = parse_data(final_path)
    except Exception as e:
        print(f"Error parsing data: {e}")
        continue_script=False
        original_fieldnames=None
        final_fieldnames=None
        original_row_id=None
        final_row_id=None
        original_data=None
        final_data=None
    return {
                'continue_script':continue_script,
                'original_fieldnames': original_fieldnames,
                'final_fieldnames': final_fieldnames,
                'original_row_id': original_row_id,
                'final_row_id': final_row_id,
                'original_data': original_data,
                'final_data': final_data
            }






# original_duplicate_fieldnames, original_unique_fieldnames = separate_duplicate_values(original_fieldnames, 'Original Fieldnames').values()
# write_list_csv('Original Duplicate Fieldnames', original_duplicate_fieldnames, results_path)

# final_duplicate_fieldnames, final_unique_fieldnames = separate_duplicate_values(final_fieldnames, 'Final Fieldnames').values()
# write_list_csv('Final Duplicate Fieldnames', final_duplicate_fieldnames, results_path)

# original_unmatched_fieldnames, final_unmatched_fieldnames, comparison_fieldnames = separate_unmatched_values(original_unique_fieldnames, final_unique_fieldnames, original_duplicate_fieldnames, final_duplicate_fieldnames, 'fieldnames').values()
# write_list_csv("Original Unmatched Fieldnames, original_unmatched_fieldnames, results_path)
# write_list_csv("Final Unmatched Fieldnames, final_unmatched_fieldnames, results_path)

# original_duplicate_row_id, original_unique_row_id = separate_duplicate_values(original_row_id, 'Original Row ID').values()
# write_list_csv('Original Duplicate Row ID', original_duplicate_row_id, results_path)

# final_duplicate_row_id, final_unique_row_id = separate_duplicate_values(final_row_id, 'Final Row ID').values()
# write_list_csv('Final Duplicate Row ID', final_duplicate_row_id, results_path)

# original_unmatched_row_id, final_unmatched_row_id, comparison_row_id = separate_unmatched_values(original_unique_row_id, final_unique_row_id, original_duplicate_row_id, final_duplicate_row_id, 'row ID').values()
# write_list_csv("Original Unmatched Row ID", original_unmatched_row_id, results_path)
# write_list_csv("Final Unmatched Row ID", final_unmatched_row_id, results_path)



# comparison_writer(original_data, final_data, comparison_fieldnames, comparison_row_id, results_path)
