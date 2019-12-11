from ..models import AutopsyTypes, TissueTypes, NeuropathologicalDiagnosis


# This class get result from models or insert new data if it doesn't found anything
# Following models are used: AutopsyTypes, TissueTypes, NeuropathologicalDiagnosis
class GetOrCreate(object):

    def __init__(self, **kwargs):
        self.model_name = kwargs.get('model_name', None)
        self.models = {
            'AutopsyTypes': AutopsyTypes, 'TissueTypes': TissueTypes,
            'NeuropathologicalDiagnosis': NeuropathologicalDiagnosis
        }

    def run(self, **kwargs):
        try:
            model_object = self.models[self.model_name].objects.get(**kwargs)
            return model_object

        except self.models[self.model_name].DoesNotExist:
            model_object = self.models[self.model_name].objects.create(**kwargs)
            return model_object