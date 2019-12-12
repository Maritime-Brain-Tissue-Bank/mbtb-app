class ValidateData(object):

    # Check if received file is of type CSV; return true if it is else false
    def check_file_type(self, **kwargs):
        _file_name = kwargs.get('filename', None)
        _file_name = _file_name.split('.')
        if _file_name[-1] == 'csv':
            return {'Response': True}
        return {'Response': False, 'Message': 'Wrong file type, please upload CSV file'}

    # Check if request contain `file` tag; return true if it matches else false
    def check_file_tag(self, **kwargs):
        request = kwargs.get('request', None)
        if request.data.__contains__('file'):
            if len(request.data.__getitem__('file')) > 0:
                return {'Response': True}
            return {'Response': False, 'Message': "File can't be empty, Please upload again."}
        return {'Response': False, 'Message': 'File not found, please upload CSV file'}

    # Check for received dict size and its elements
    def check_file_size(self, **kwargs):
        csv_file = kwargs.get('csv_file', None)
        if len(csv_file) != 0:
            for row in csv_file:
                if len(row) != 26:
                    return {'Response': False, 'Message': 'Not enough elements are present in single row.'}
            return {'Response': True}
        return {'Response': False, 'Message': 'Error in file size, please upload valid file.'}

    # Compare column names with actual ones; return true if it matches else false
    def check_column_names(self, **kwargs):
        received_column_names = kwargs.get('column_names', None)
        actual_column_names = [
            'mbtb_code', 'sex', 'age', 'postmortem_interval', 'time_in_fix', 'clinical_diagnosis',
            'preservation_method', 'storage_year', 'tissue_type', 'neuropathology_diagnosis', 'race', 'duration',
            'clinical_details', '', 'cause_of_death', 'brain_weight', 'neuropathology_summary', 'neuropathology_gross',
            'neuropathology_microscopic', 'cerad', 'braak_stage', 'khachaturian', 'abc', 'formalin_fixed',
            'fresh_frozen', 'autopsy_type'
        ]

        if actual_column_names == received_column_names:
            return {'Response': True}
        return {'Response': False, 'Message': "Column names don't match, Please try again with valid names."}

    