class PrimeDetailsTemplate(object):

    def __init__(self, **kwargs):
        self.mbtb_code = kwargs.get('mbtb_code', None)
        self.sex = kwargs.get('sex', None)
        self.age = kwargs.get('age', None)
        self.postmortem_interval = kwargs.get('postmortem_interval', None)
        self.time_in_fix = kwargs.get('time_in_fix', None)
        self.clinical_diagnosis = kwargs.get('clinical_diagnosis', None)
        self.tissue_type = kwargs.get('tissue_type', None)
        self.preservation_method = kwargs.get('preservation_method', None)
        self.neuro_diagnosis_id = kwargs.get('neuro_diagnosis_id', None)
        self.storage_year = kwargs.get('storage_year', None)
