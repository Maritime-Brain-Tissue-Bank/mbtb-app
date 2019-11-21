from rest_framework import viewsets, views, response
from .permissions import IsAuthenticated

from .models import AutopsyType, BrainDataset, DatasetOthrDetails, ImageRepository, NeurodegenerativeDiseases, \
    TissueType
from .serializers import BrainDatasetSerializer, DatasetOtherDetailsSerializer


class BrainDatasetAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BrainDataset.objects.all()
    serializer_class = BrainDatasetSerializer


class DatasetOthrDetailsAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DatasetOthrDetails.objects.all()
    serializer_class = DatasetOtherDetailsSerializer
    lookup_field = 'brain_data_id'


class CreateDataAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return response.Response({'Error': "Please provide mbtb data"}, status="400")

        try:
            _mbtb_code = request.data['mbtb_code']
            _sex = request.data['sex']
            _age = request.data['age']
            _postmortem_interval = request.data['postmortem_interval']
            _time_in_fix = request.data['time_in_fix']
            _storage_method = request.data['storage_method']
            _race = request.data['race']
            _diagnosis = request.data['diagnosis']
            _duration = request.data['duration']
            _clinical_history = request.data['clinical_history']
            _cause_of_death = request.data['cause_of_death']
            _brain_weight = request.data['brain_weight']
            _neuoropathology_detailed = request.data['neuoropathology_detailed']
            _neuropathology_gross = request.data['neuropathology_gross']
            _neuropathology_micro = request.data['neuropathology_micro']
            _neouropathology_criteria = request.data['neouropathology_criteria']
            _cerad = request.data['cerad']
            _braak_stage = request.data['braak_stage']
            _khachaturian = request.data['khachaturian']
            _abc = request.data['abc']
            _formalin_fixed = request.data['formalin_fixed']
            _fresh_frozen = request.data['fresh_frozen']
            _autopsy_type = request.data['autopsy_type']
            _tissue_type = request.data['tissue_type']
            _neuoropathology_diagnosis = request.data['neuoropathology_diagnosis']

            # fetching ids for: autopsy_type, tissue_type, neuro_disease
            self.autopsy_type = AutopsyType.objects.get(autopsy_type=_autopsy_type)
            self.tissue_type = TissueType.objects.get(tissue_type=_tissue_type)
            self.disease_name = NeurodegenerativeDiseases.objects.get(disease_name=_neuoropathology_diagnosis)

            # Inserting new data: BrainDataset, DatasetOthrDetails
            self.brain_data = BrainDataset.objects.create(
                mbtb_code=_mbtb_code, sex=_sex, age=_age, postmortem_interval=_postmortem_interval,
                time_in_fix=_time_in_fix, storage_method=_storage_method,
                neuro_diseases_id=self.disease_name, tissue_type_id=self.tissue_type.pk
            )
            self.dataset_other_details = DatasetOthrDetails.objects.create(
                brain_data_id=self.brain_data, autopsy_type=self.autopsy_type,
                race=_race, diagnosis=_diagnosis, duration=_duration, clinical_history=_clinical_history,
                cause_of_death=_cause_of_death, brain_weight=_brain_weight,
                neuoropathology_detailed=_neuoropathology_detailed, neuropathology_gross=_neuropathology_gross,
                neuropathology_micro=_neuropathology_micro, neouropathology_criteria=_neouropathology_criteria,
                cerad=_cerad, braak_stage=_braak_stage, khachaturian=_khachaturian, abc=_abc,
                formalin_fixed=_formalin_fixed, fresh_frozen=_fresh_frozen,
            )
            return response.Response({'Response': "Success"}, status="200")

        except (KeyError, BaseException, AutopsyType.DoesNotExist, TissueType.DoesNotExist,
                NeurodegenerativeDiseases.DoesNotExist) as e:
            return response.Response({'Error': "Either missing fields or incorrect data"}, status="400")
