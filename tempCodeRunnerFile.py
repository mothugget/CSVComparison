ORIGINAL_FIELDNAMES = read_fieldnames('original.csv')
FINAL_FIELDNAMES = read_fieldnames('final.csv')

ORIGINAL_ROW_ID=read_row_id('original.csv','id')
FINAL_ROW_ID=read_row_id('final.csv','id')

ORIGINAL_DATA=parse_data('original.csv')
FINAL_DATA=parse_data('final.csv')

unmatched_fieldname_results=separate_unmatched_values(ORIGINAL_FIELDNAMES,FINAL_FIELDNAMES,'fieldnames')
ORIGINAL_UNMATCHED_FIELDNAMES=unmatched_fieldname_results['original_unmatched']
FINAL_UNMATCHED_FIELDNAMES=unmatched_fieldname_results['final_unmatched']
COMPARISON_FIELDNAMES=unmatched_fieldname_results['comparison']

write_list_csv("Original Unmatched Fieldnames", ORIGINAL_UNMATCHED_FIELDNAMES, RESULTS_PATH)
write_list_csv("Final Unmatched Fieldnames", FINAL_UNMATCHED_FIELDNAMES, RESULTS_PATH)

unmatched_row_id_results=separate_unmatched_values(ORIGINAL_ROW_ID,FINAL_ROW_ID,'row ID')
ORIGINAL_UNMATCHED_ROW_ID=unmatched_row_id_results['original_unmatched']
FINAL_UNMATCHED_ROW_ID=unmatched_row_id_results['final_unmatched']
COMPARISON_ROW_ID=unmatched_row_id_results['comparison']

write_list_csv("Original Unmatched Row ID", ORIGINAL_UNMATCHED_ROW_ID, RESULTS_PATH)
write_list_csv("Final Unmatched Row ID", FINAL_UNMATCHED_ROW_ID, RESULTS_PATH)

comparison_writer(ORIGINAL_DATA,FINAL_DATA,COMPARISON_FIELDNAMES,COMPARISON_ROW_ID,RESULTS_PATH)
