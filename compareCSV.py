import csv
import datetime
import os

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

def read_csv_data(props):
    continue_to_next_function=True
    try:
        if props['original_path']==None:
            props['original_path']='original.csv'
        if props['final_path']==None:
            props['final_path']='final.csv'
        original_fieldnames = read_fieldnames(props['original_path'])
        if props['id_fieldname']==None:
            id_fieldname=original_fieldnames[0]
        else:
            id_fieldname=props['id_fieldname']
        final_fieldnames = read_fieldnames(props['final_path'])
        original_row_id = read_row_id(props['original_path'], id_fieldname)   
        final_row_id = read_row_id(props['final_path'], id_fieldname)    
        original_data = parse_data(props['original_path'])    
        final_data = parse_data(props['final_path'])
    except Exception as e:
        print(f"Error parsing data: {e}")
        continue_to_next_function=False
        original_fieldnames=None
        final_fieldnames=None
        original_row_id=None
        final_row_id=None
        original_data=None
        final_data=None
    return {
                'continue_process_csv':continue_to_next_function,
                'parsed_csv':{
                    'original_fieldnames': original_fieldnames,
                    'final_fieldnames': final_fieldnames,
                    'original_row_id': original_row_id,
                    'final_row_id': final_row_id,
                    'original_data': original_data,
                    'final_data': final_data
                }
            }

def true_false_input(prompt):
    try_again=True
    try_counter=0
    while try_again==True and try_counter<3:
        try_counter+=1
        try:
            input_value:bool=eval(input(prompt+'\n(True/False)'))
            try_again=False
            return_object = {'input':input_value,'valid_input':True}
        except Exception as e:
            print(f"Sorry, didn't quite catch that. Remember answers are case sensitive \n {e}\n")
            if try_counter==3:
                print("You've tried this three times now. I'm giving up on you.")
                return_object =  {'input':None,'valid_input':False}
    return return_object

def try_again():
    try_again_input=true_false_input('Would you like to try again?')
    if try_again_input['valid_input']:
        return try_again_input['input']
    else:return False

def extract_duplicate_and_unmatched_values(props):
    continue_comparison = True
    try:
        
        original_duplicate_fieldnames, original_unique_fieldnames = separate_duplicate_values(props['original_fieldnames'], 'Original Fieldnames').values()
        write_list_csv('Original Duplicate Fieldnames', original_duplicate_fieldnames, props['results_path'])

        final_duplicate_fieldnames, final_unique_fieldnames = separate_duplicate_values(props['final_fieldnames'], 'Final Fieldnames').values()
        write_list_csv('Final Duplicate Fieldnames', final_duplicate_fieldnames, props['results_path'])

        original_unmatched_fieldnames, final_unmatched_fieldnames, comparison_fieldnames = separate_unmatched_values(original_unique_fieldnames, final_unique_fieldnames, original_duplicate_fieldnames, final_duplicate_fieldnames, 'fieldnames').values()
        write_list_csv("Original Unmatched Fieldnames", original_unmatched_fieldnames, props['results_path'])
        write_list_csv("Final Unmatched Fieldnames", final_unmatched_fieldnames, props['results_path'])

        original_duplicate_row_id, original_unique_row_id = separate_duplicate_values(props['original_row_id'], 'Original Row ID').values()
        write_list_csv('Original Duplicate Row ID', original_duplicate_row_id, props['results_path'])

        final_duplicate_row_id, final_unique_row_id = separate_duplicate_values(props['final_row_id'], 'Final Row ID').values()
        write_list_csv('Final Duplicate Row ID', final_duplicate_row_id, props['results_path'])

        original_unmatched_row_id, final_unmatched_row_id, comparison_row_id = separate_unmatched_values(original_unique_row_id, final_unique_row_id, original_duplicate_row_id, final_duplicate_row_id, 'row ID').values()
        write_list_csv("Original Unmatched Row ID", original_unmatched_row_id, props['results_path'])
        write_list_csv("Final Unmatched Row ID", final_unmatched_row_id, props['results_path'])
        return {'continue_comparison':continue_comparison,'comparison_fieldnames':comparison_fieldnames,'comparison_row_id':comparison_row_id}
    except Exception as e:
        continue_comparison=False
        print('Something went wrong\n'+e)
        return {'continue_comparison':continue_comparison,'comparison_fieldnames':None,'comparison_row_id':None}

#Script starts here

print('Welcome to the CSV comparison script')
run_script:bool = True
continue_read_csv=True
while run_script == True:
    read_csv_props = {
        'original_path':None,
        'final_path':None,
        'id_fieldname':None}
    results_path = 'Results'
    print('By default, this script looks at the directory in which it resides. It compares .csv files named original.csv and final.csv, and creates a folder with the results in the same directory.')
    custom_config=true_false_input('Would you like to add your own custom config?')
    continue_read_csv=custom_config['valid_input']
    if continue_read_csv and custom_config['input']:
        try:
            read_csv_props=eval(input("{'original_path': '/Users/karlfredriksson/tdcc/original.csv','final_path': '/Users/karlfredriksson/tdcc/final.csv','id_fieldname':'id','results_path':'/Users/karlfredriksson/tdcc'}\n"))
            results_path=read_csv_props['results_path']
        except Exception as e:
            print(f'There seems to be an error \n{e}\n')
            continue_read_csv=False
            run_script=try_again()
    continue_process_csv=False
    if continue_read_csv:
        csv_results=read_csv_data(read_csv_props)
    continue_process_csv=csv_results['continue_process_csv']
    parsed_csv=csv_results['parsed_csv']
    parsed_csv['results_path']=results_path
    comparison_data={'continue_comparison':False}
    if continue_process_csv:
        comparison_data=extract_duplicate_and_unmatched_values(parsed_csv)
    else:
        run_script=try_again()
    if comparison_data['continue_comparison']:
        comparison_writer(parsed_csv['original_data'], parsed_csv['final_data'], comparison_data['comparison_fieldnames'], comparison_data['comparison_row_id'], results_path)
        run_script=False
    else:
        run_script=try_again()




