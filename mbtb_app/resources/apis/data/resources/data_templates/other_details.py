class OtherDetailsTemplate(object):

    def __init__(self, **kwargs):
        self.prime_details_id = kwargs.get('prime_details_id', '')
        self.race = kwargs.get('race', '')
        self.duration = kwargs.get('duration', '')
        self.clinical_details = kwargs.get('clinical_details', '')
        self.cause_of_death = kwargs.get('cause_of_death', '')
        self.brain_weight = kwargs.get('brain_weight', '')
        self.neuropathology_summary = kwargs.get('neuropathology_summary', '')
        self.neuropathology_gross = kwargs.get('neuropathology_gross', '')
        self.neuropathology_microscopic = kwargs.get('neuropathology_microscopic', '')
        self.cerad = kwargs.get('cerad', '')
        self.braak_stage = kwargs.get('braak_stage', '')
        self.khachaturian = kwargs.get('khachaturian', '')
        self.abc = kwargs.get('abc', '')
        self.autopsy_type = kwargs.get('autopsy_type', '')
        self.formalin_fixed = kwargs.get('formalin_fixed', '')
        self.fresh_frozen = kwargs.get('fresh_frozen', '')
