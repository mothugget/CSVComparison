import csv
import datetime
import os
import json
import time

def read_fieldnames(file_path,custom_delimiter,custom_quote_character):
    print('Reading ' + file_path + ' fieldnames')
    fieldnames = []
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile,delimiter=custom_delimiter, quotechar=custom_quote_character)
        for row in csv_reader:
            fieldnames = row
            break
    print('Finished reading ' + file_path + ' fieldnames')
    return fieldnames

def read_row_id(file_path, id_fieldname,custom_delimiter,custom_quote_character):
    print('Reading ' + file_path + ' row IDs')
    id_list = []
    with open(file_path, 'r') as csvdictfile:
        dict_csv_reader = csv.DictReader(csvdictfile,delimiter=custom_delimiter, quotechar=custom_quote_character)
        for row in dict_csv_reader:
            id_list.append(row[id_fieldname])
    print('Finished reading ' + file_path + ' row IDs')
    return id_list

def parse_data(file_path,id_fieldname,custom_delimiter,custom_quote_character):
    print('Parsing ' + file_path + ' data')
    data_dict = {}
    with open(file_path, 'r') as csvdictfile:
        dict_csv_reader = csv.DictReader(csvdictfile,delimiter=custom_delimiter, quotechar=custom_quote_character)
        for row in dict_csv_reader:
            data_dict[row[id_fieldname]] = row
    print('Finished parsing ' + file_path + ' data')
    return data_dict

def separate_duplicate_values(list, type):
    start=time.time()
    print('Analysing duplicate ' + type)
    duplicates = {}
    unique = {}
    for value in list:
        if value in duplicates:
            duplicates[value]+=1
        elif value in unique:
            del unique[value]
            duplicates[value]=2
        else:
            unique[value]=True
    print('\nFinished analysing duplicate ' + type+' in', time.time()-start,'seconds\n')
    return {'duplicates': duplicates, 'unique': unique}

def separate_unmatched_values(original, final, original_duplicates, type):
    start=time.time()
    print('Analysing unmatched ' + type)
    matched = []
    original_unmatched = []
    final_unmatched = final.copy()

    for key in list(original.keys()):
        if key in final:
            matched.append(key)
            del final_unmatched[key]
        else:
            original_unmatched.append(key)

    for key in list(final_unmatched.keys()):
        if key in original_duplicates:
            del final_unmatched[key]
  

    print('\nFinished analysing unmatched ' + type+' in', time.time()-start,'seconds\n')
    return {
        'original_unmatched': original_unmatched,
        'final_unmatched': list(final_unmatched.keys()),
        'comparison': matched
    }

def create_results_folder(results_containing_directory_path,original_filepath,final_filepath):
    try:
        print('Creating results folder')
        result_path = os.path.join(results_containing_directory_path,'Results - ('+ os.path.basename(original_filepath)+ " || " + os.path.basename(final_filepath) + ") " + str(datetime.datetime.today())[0:19])
        os.makedirs(result_path)
        print("Results folder created")
        return {'continue_process_csv':True,'generated_path':result_path}
    except  Exception as e:
        print('Something went wrong \n',e) 
        return {'continue_process_csv':False, 'generated_path':None}

def write_list_csv(title, write_list, results_path):
    print('Creating ' + title + ' result csv')
    write_list.insert(0, title)
    with open(os.path.join(results_path, title + '.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for value in write_list:
            csv_writer.writerow([value])
    print('Created ' + title + ' result csv')

def write_dict_csv(title, value_title, dict, results_path):
    print('Creating ' + title + ' result csv')
    write_list=[[title,value_title]]
    for key in list(dict.keys()):
        write_list.append([key,dict[key]])
    with open(os.path.join(results_path,title+'.csv'), 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in write_list:
            csv_writer.writerow(row)
    print('Created ' + title + ' result csv')

def comparison_writer(original_data, final_data, comparison_fieldnames, comparison_row_id, results_path):
    try:
        start=time.time()
        print('Comparing Data')
        result_fieldnames = comparison_fieldnames[:]
        result_fieldnames.insert(0, 'Sheet Comparison Row ID')

        with open(os.path.join(results_path,'Sheet Comparison.csv'), 'w') as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames = result_fieldnames)
            csv_writer.writeheader()
            for id in comparison_row_id:
                compared_row = row_comparison(id, original_data, final_data, comparison_fieldnames)
                if compared_row['differences']:
                    csv_writer.writerow(compared_row['row_object'])
        print('\nFinished Comparing Data in\n\n', time.time()-start,'seconds\n')
    except Exception as e:
        print('\nSomething went wrong\n',e)

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
        original_fieldnames = read_fieldnames(props['original_path'],props['original_delimiter'],props['original_quote_character'])
        final_fieldnames = read_fieldnames(props['final_path'],props['final_delimiter'],props['final_quote_character'])
        id_fieldname=find_unique_matched_id_fieldname(props['id_fieldname'], original_fieldnames, final_fieldnames)
        original_row_id = read_row_id(props['original_path'], id_fieldname,props['original_delimiter'],props['original_quote_character'])   
        final_row_id = read_row_id(props['final_path'], id_fieldname,props['final_delimiter'],props['final_quote_character'])    
        original_data = parse_data(props['original_path'],id_fieldname,props['original_delimiter'],props['original_quote_character'])    
        final_data = parse_data(props['final_path'],id_fieldname,props['final_delimiter'],props['final_quote_character'])
    except Exception as e:
        print("\nError parsing data:",e)
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
            print("\nSorry, didn't quite catch that. Remember answers are case sensitive \n", e,"\n")
            if try_counter==3:
                print("You've tried this three times now. I'm giving up on you.")
                return_object =  {'input':None,'valid_input':False}
    return return_object

def try_again():
    try_again_input=true_false_input('\nWould you like to run the script again?')
    if try_again_input['valid_input']:
        return try_again_input['input']
    else:return False

def extract_duplicate_and_unmatched_values(props):
    skipped_categories=[]
    try:

        original_duplicate_fieldnames, original_unique_fieldnames = separate_duplicate_values(props['original_fieldnames'], 'Original Fieldnames').values()
        original_duplicate_fieldnames=={} or (skipped_categories.append('Original Duplicate Fieldnames') or write_dict_csv('Original Duplicate Fieldnames', 'Count',original_duplicate_fieldnames, props['results_path']))
        
        final_duplicate_fieldnames, final_unique_fieldnames = separate_duplicate_values(props['final_fieldnames'], 'Final Fieldnames').values()
        final_duplicate_fieldnames=={} or (skipped_categories.append('Final Duplicate Fieldnames') or write_dict_csv('Final Duplicate Fieldnames', 'Count', final_duplicate_fieldnames, props['results_path']))
        
        original_unmatched_fieldnames, final_unmatched_fieldnames, comparison_fieldnames = separate_unmatched_values(original_unique_fieldnames, final_unique_fieldnames, list(original_duplicate_fieldnames.keys()), 'fieldnames').values()
        original_unmatched_fieldnames==[] or (skipped_categories.append('Original Unmatched Fieldnames') or write_list_csv("Original Unmatched Fieldnames", original_unmatched_fieldnames, props['results_path']))
        final_unmatched_fieldnames==[] or (skipped_categories.append('Final Unmatched Fieldnames') or write_list_csv("Final Unmatched Fieldnames", final_unmatched_fieldnames, props['results_path']))

        original_duplicate_row_id, original_unique_row_id = separate_duplicate_values(props['original_row_id'], 'Original Row ID').values()
        original_duplicate_row_id=={} or (skipped_categories.append('Original Duplicate Row ID') or write_dict_csv('Original Duplicate Row ID', 'Count', original_duplicate_row_id, props['results_path']))
        
        final_duplicate_row_id, final_unique_row_id = separate_duplicate_values(props['final_row_id'], 'Final Row ID').values()
        final_duplicate_row_id=={} or (skipped_categories.append('Final Duplicate Row ID') or write_dict_csv('Final Duplicate Row ID', 'Count', final_duplicate_row_id, props['results_path']))
        
        original_unmatched_row_id, final_unmatched_row_id, comparison_row_id = separate_unmatched_values(original_unique_row_id, final_unique_row_id, list(original_duplicate_row_id.keys()), 'row ID').values()
        original_unmatched_row_id==[] or (skipped_categories.append('Original Unmatched Row ID') or write_list_csv("Original Unmatched Row ID", original_unmatched_row_id, props['results_path']))
        final_unmatched_row_id==[] or (skipped_categories.append('Final Unmatched Row ID') or write_list_csv("Final Unmatched Row ID", final_unmatched_row_id, props['results_path']))
        
        return {'continue_comparison':True,'comparison_fieldnames':comparison_fieldnames,'comparison_row_id':comparison_row_id, 'skipped_categories':skipped_categories}
    
    except Exception as e:
        print('\nSomething went wrong\n',e)
        return {'continue_comparison':False,'comparison_fieldnames':None,'comparison_row_id':None,'skipped_categories':skipped_categories}

def write_json_config_file(config_dict):
    if not os.path.isfile('CSVComparisonConfig.json'):
        with open("CSVComparisonConfig.json", "w") as outfile:
            json.dump(config_dict, outfile)

def write_json_config_results_file(config_dict,results_path):
    with open(os.path.join(results_path,"UsedCSVComparisonConfig.json"), "w") as outfile:
        json.dump(config_dict, outfile)

def read_json_config_file():
        with open("CSVComparisonConfig.json", "r") as infile:
            return json.load(infile)

def is_list_subset(subset, set):
    missing_values=[x for x in subset if set.count(x)==0]
    return missing_values==[]

def is_element_duplicate_or_unmatched(element,original_list,final_list):
    original_count=original_list.count(element)
    final_count=final_list.count(element)
    result={'duplicate_or_unmatched':False,'message':[]}
    if original_count>1:
        result['duplicate_or_unmatched']=True
        result['message'].append('Duplicate in the original data')
    if original_count<1:
        result['duplicate_or_unmatched']=True
        result['message'].append('Unmatched in the original data')
    if final_count>1:
        result['duplicate_or_unmatched']=True
        result['message'].append('Duplicate in the final data')
    if final_count<1:
        result['duplicate_or_unmatched']=True
        result['message'].append('Unmatched in the final data')
    return result

def find_unique_matched_id_fieldname(proposed_id_fieldname,original_fieldname_list,final_fieldname_list):
    if proposed_id_fieldname==None:
        for value in original_fieldname_list:
            if original_fieldname_list.count(value)==1 and final_fieldname_list.count(value)==1:
                return value
        raise Exception('No fieldname could be found which is both unique and matched in both the original and final data.')
    result=is_element_duplicate_or_unmatched(proposed_id_fieldname,original_fieldname_list,final_fieldname_list)
    if result['duplicate_or_unmatched']:
        raise Exception('The specified fieldname was rejected for the following reasons:\n\n'+'\n'.join(result['message']))
    return proposed_id_fieldname


#Script starts here

print('\n\nWelcome to the CSV comparison script\n')
run_script:bool = True
while run_script == True:
    default_config = {
        'original_path':'original.csv',
        'original_delimiter':',',
        'original_quote_character':'"',
        'final_path':'final.csv',
        'final_delimiter':',',
        'final_quote_character':'"',
        'id_fieldname':None,
        'results_path':''
        }
    continue_read_csv=True
    try:
        write_json_config_file(default_config)
        print('By default, this script looks at the directory in which it is being run.\nIt compares .csv files named original.csv and final.csv, and creates a folder with the results in the same directory.\n\nIf you wish to change any of these paths, or any other parameters, please see the file CSVComparisonConfig.json\nThe fieldnames are taken from the first row of the .csv files.\nIf no other value is specified, the fieldname of the values used to ID the rows of the CSV file is the first fieldname of the original file.\n')
        input('When the files and configurations are ready, press enter to continue:')
        read_csv_props = read_json_config_file()
        if not is_list_subset(list(default_config.keys()), list(read_csv_props.keys())):
            raise Exception('Config file is missing keys. To restart from a default config file, delete CSVComparisonConfig.json from the directory in which this script is running.') 
        results_path = read_csv_props['results_path']
    except Exception as e:
        print('\nSomething went wrong\n',e)
        continue_read_csv=False
    if continue_read_csv:
        csv_results=read_csv_data(read_csv_props)
        if csv_results['continue_process_csv']:
            generated_results_folder=create_results_folder(results_path,read_csv_props['original_path'],read_csv_props['final_path'])
            csv_results['parsed_csv']['results_path']=generated_results_folder['generated_path']
            write_json_config_results_file(read_csv_props,generated_results_folder['generated_path'])
            if generated_results_folder['continue_process_csv']:
                comparison_data=extract_duplicate_and_unmatched_values(csv_results['parsed_csv'])
                if comparison_data['continue_comparison']==False:
                    run_script=try_again()
                elif comparison_data['skipped_categories']!=[]:
                    print('\n\tOBSERVE:\nFieldnames and row ID need to be unique and present on both sheets in order to compare the data.\nSome fieldnames/row ID were duplicates or unmatched, and so the corresponding rows/columns will be skipped in the final analysis.\nThese can be found in the results folder, under the following headings:\n')
                    for category in comparison_data['skipped_categories']:
                        print(category)
                    print('\nPlease verify the contents of these files as this data will not be part of the final comparison.')
                    continue_input=true_false_input('\nWould you like to continue the comparison?')
                    if continue_input['valid_input']:
                        comparison_data['continue_comparison']=continue_input['input']
                    else:
                        comparison_data['continue_comparison']=False
                if comparison_data['continue_comparison']:
                    comparison_writer(csv_results['parsed_csv']['original_data'], csv_results['parsed_csv']['final_data'], comparison_data['comparison_fieldnames'], comparison_data['comparison_row_id'], csv_results['parsed_csv']['results_path'])
                    run_script=False
                else:
                    run_script=False
            else: 
                run_script=try_again()
        else:
            run_script=try_again()
    else:
        run_script=try_again()