from rest_framework import viewsets, views, response
from .permissions import IsAuthenticated

from .models import AutopsyTypes, PrimeDetails, OtherDetails, NeuropathologicalDiagnosis, \
    TissueTypes
from .serializers import PrimeDetailsSerializer, OtherDetailsSerializer


class PrimeDetailsAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PrimeDetails.objects.all()
    serializer_class = PrimeDetailsSerializer


class OtherDetailsAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OtherDetails.objects.all()
    serializer_class = OtherDetailsSerializer
    lookup_field = 'prime_details_id'


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
            _preservation_method = request.data['preservation_method']
            _race = request.data['race']
            _clinical_diagnosis = request.data['clinical_diagnosis']
            _duration = request.data['duration']
            _clinical_details = request.data['clinical_details']
            _cause_of_death = request.data['cause_of_death']
            _brain_weight = request.data['brain_weight']
            _neuoropathology_summary = request.data['neuoropathology_summary']
            _neuropathology_gross = request.data['neuropathology_gross']
            _neuropathology_microscopic = request.data['neuropathology_microscopic']
            _cerad = request.data['cerad']
            _braak_stage = request.data['braak_stage']
            _khachaturian = request.data['khachaturian']
            _abc = request.data['abc']
            _formalin_fixed = request.data['formalin_fixed']
            _fresh_frozen = request.data['fresh_frozen']
            _autopsy_type = request.data['autopsy_type']
            _tissue_type = request.data['tissue_type']
            _neuropathology_diagnosis = request.data['neuropathology_diagnosis']

            # fetching ids for: autopsy_type, tissue_type, neuro_disease
            self.autopsy_type = AutopsyTypes.objects.get(autopsy_type=_autopsy_type)
            self.tissue_type = TissueTypes.objects.get(tissue_type=_tissue_type)
            self.neuro_diagnosis_name = NeuropathologicalDiagnosis.objects.get(neuro_diagnosis_name=_neuropathology_diagnosis)

            # Inserting new data: PrimeDetails, OtherDetails
            self.prime_details = PrimeDetails.objects.create(
                mbtb_code=_mbtb_code, sex=_sex, age=_age, postmortem_interval=_postmortem_interval,
                time_in_fix=_time_in_fix, preservation_method=_preservation_method,
                clinical_diagnosis=_clinical_diagnosis, neuro_diagnosis_id=self.neuro_diagnosis_name,
                tissue_type_id=self.tissue_type.pk
            )
            self.other_details = OtherDetails.objects.create(
                prime_details_id=self.prime_details, autopsy_type=self.autopsy_type,
                race=_race, duration=_duration, clinical_details=_clinical_details, cause_of_death=_cause_of_death,
                brain_weight=_brain_weight, neuoropathology_summary=_neuoropathology_summary,
                neuropathology_gross=_neuropathology_gross, neuropathology_microscopic=_neuropathology_microscopic,
                cerad=_cerad, braak_stage=_braak_stage, khachaturian=_khachaturian, abc=_abc,
                formalin_fixed=_formalin_fixed, fresh_frozen=_fresh_frozen,
            )
            return response.Response({'Response': "Success"}, status="200")

        except (KeyError, BaseException, AutopsyTypes.DoesNotExist, TissueTypes.DoesNotExist,
                NeuropathologicalDiagnosis.DoesNotExist) as e:
            return response.Response({'Error': "Either missing fields or incorrect data"}, status="400")


class GetSelectOptions(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        _neuropathology_diagnosis = NeuropathologicalDiagnosis.objects.values_list('neuro_diagnosis_name', flat=True).order_by('neuro_diagnosis_name')
        _autopsy_type = AutopsyTypes.objects.values_list('autopsy_type', flat=True).order_by('autopsy_type')
        _tissue_type = TissueTypes.objects.values_list('tissue_type', flat=True).order_by('tissue_type')

        return response.Response({
            'neuropathology_diagnosis': _neuropathology_diagnosis,
            'autopsy_type': _autopsy_type,
            'tissue_type': _tissue_type
        })
