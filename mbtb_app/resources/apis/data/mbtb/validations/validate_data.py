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
        _request = kwargs.get('request', None)
        if _request.data.__contains__('file'):
            if len(_request.data.__getitem__('file')) > 0:
                return {'Response': True}
            return {'Response': False, 'Message': "File can't be empty, Please upload again."}
        return {'Response': False, 'Message': 'File not found, please upload CSV file'}

    # Check for received dict size and its elements
    def check_file_size(self, **kwargs):
        _csv_file = kwargs.get('csv_file', None)
        if len(_csv_file) != 0:
            for row in _csv_file:
                if len(row) != 25:
                    return {'Response': False, 'Message': 'Not enough elements are present in single row.'}
            return {'Response': True}
        return {'Response': False, 'Message': 'Error in file size, please upload valid file.'}

    # Compare column names with actual ones; return true if it matches else false
    def check_column_names(self, **kwargs):
        _received_column_names = kwargs.get('column_names', None)
        _actual_column_names = [
            'mbtb_code', 'sex', 'age', 'postmortem_interval', 'time_in_fix', 'clinical_diagnosis',
            'preservation_method', 'storage_year', 'tissue_type', 'neuropathology_diagnosis', 'race', 'duration',
            'clinical_details', 'cause_of_death', 'brain_weight', 'neuropathology_summary', 'neuropathology_gross',
            'neuropathology_microscopic', 'cerad', 'braak_stage', 'khachaturian', 'abc', 'formalin_fixed',
            'fresh_frozen', 'autopsy_type'
        ]
        difference = list(set(_actual_column_names) - set(_received_column_names))

        # TODO: Once `storage_year` added in insert single row, need to rewrite below logic.
        if len(difference) > 0:
            # Check condition for insert single row; return true if `storage_year` is the only difference
            if 'storage_year' in difference and len(difference) is 1:
                return {'Response': True}
            else:
                if 'storage_year' in difference:
                    difference.pop(difference.index('storage_year'))
                return {
                    'Response': False,
                    'Message': "Column names don't match with following: {}, Please try again with valid names.".
                        format(difference)
                }
        return {'Response': True}
