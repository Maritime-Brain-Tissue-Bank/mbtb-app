import codecs
import csv

from rest_framework import viewsets, views, response
from rest_framework.parsers import MultiPartParser, FormParser
from .data_templates.other_details import OtherDetailsTemplate
from .data_templates.prime_details import PrimeDetailsTemplate
from .db_operations.get_or_create import GetOrCreate
from .permissions import IsAuthenticated
from .models import AutopsyTypes, PrimeDetails, OtherDetails, NeuropathologicalDiagnosis, \
    TissueTypes
from .serializers import PrimeDetailsSerializer, OtherDetailsSerializer, FileUploadPrimeDetailsSerializer, \
    FileUploadOtherDetailsSerializer, InsertRowPrimeDetailsSerializer


# This view class is to fetch prime_details, allowed methods: GET
class PrimeDetailsAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PrimeDetails.objects.all()
    serializer_class = PrimeDetailsSerializer


# This view class is to fetch other_details, allowed methods: GET
class OtherDetailsAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OtherDetails.objects.all()
    serializer_class = OtherDetailsSerializer
    lookup_field = 'prime_details_id'


# This view class is to add single row in prime_details, other_details, allowed methods: POST
class CreateDataAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.data:
            return response.Response({'Error': "Please provide mbtb data"}, status="400")

        # Get or Create (Get value or create new if not exists) for AutopsyType, TissuType and Neuro Diagnosis
        tissue_type = GetOrCreate(model_name='TissueTypes').run(tissue_type=request.data['tissue_type'])
        neuro_diagnosis_id = GetOrCreate(model_name='NeuropathologicalDiagnosis').run(
            neuro_diagnosis_name=request.data['neuropathology_diagnosis'])
        autopsy_type = GetOrCreate(model_name='AutopsyTypes').run(autopsy_type=request.data['autopsy_type'])

        # If prime_details data is validated then save it else return error response
        prime_details = PrimeDetailsTemplate(
            mbtb_code=request.data['mbtb_code'], sex=request.data['sex'], age=request.data['age'],
            postmortem_interval=request.data['postmortem_interval'], time_in_fix=request.data['time_in_fix'],
            clinical_diagnosis=request.data['clinical_diagnosis'], tissue_type=tissue_type.tissue_type_id,
            preservation_method=request.data['preservation_method'],
            neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id)
        prime_details_serializer = InsertRowPrimeDetailsSerializer(data=prime_details.__dict__)

        if prime_details_serializer.is_valid():
            prime_details_serializer.save()  # Saving prime_details

            # If other_details data is validated then save it else return error response
            other_details = OtherDetailsTemplate(
                prime_details_id=prime_details_serializer.data['prime_details_id'], race=request.data['race'],
                duration=request.data['duration'], clinical_details=request.data['clinical_details'],
                cause_of_death=request.data['cause_of_death'], brain_weight=request.data['brain_weight'],
                neuropathology_summary=request.data['neuropathology_summary'],
                neuropathology_gross=request.data['neuropathology_gross'],
                neuropathology_microscopic=request.data['neuropathology_microscopic'], cerad=request.data['cerad'],
                braak_stage=request.data['braak_stage'], khachaturian=request.data['khachaturian'],
                abc=request.data['abc'], autopsy_type=autopsy_type.autopsy_type_id,
                formalin_fixed=request.data['formalin_fixed'], fresh_frozen=request.data['fresh_frozen']
            )
            other_details_serializer = FileUploadOtherDetailsSerializer(data=other_details.__dict__)
            if other_details_serializer.is_valid():
                other_details_serializer.save()  # Saving other_details
            else:
                # TODO: log errors here related to add single data for other_details
                # Return error response if any error in other_details data
                return response.Response({
                    'Error': 'Error in other details, Data uploading failed.'},
                    status="400")

        else:
            # TODO: log errors here related to add single data for prime details
            # Return error response if any error in prime_details data
            return response.Response({
                'Error': 'Error in prime_details, Data uploading failed.'},
                status="400")

        # Return response: data is uploaded successfully
        return response.Response({'Response': 'Success'}, status="201")


# This view class is to fetch data from following tables: neuropathology_diagnosis, autopsy_type, tissue_type
# allowed methods: GET
class GetSelectOptions(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        _neuropathology_diagnosis = NeuropathologicalDiagnosis.objects.values_list('neuro_diagnosis_name', flat=True) \
            .order_by('neuro_diagnosis_name')
        _autopsy_type = AutopsyTypes.objects.values_list('autopsy_type', flat=True).order_by('autopsy_type')
        _tissue_type = TissueTypes.objects.values_list('tissue_type', flat=True).order_by('tissue_type')

        return response.Response({
            'neuropathology_diagnosis': _neuropathology_diagnosis,
            'autopsy_type': _autopsy_type,
            'tissue_type': _tissue_type
        })


# This view class is to upload data via csv file in prime_details, other_details, allowed methods: POST
class FileUploadAPIView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    # TODO: Add validators here to check filed names, data
    def post(self, request, format=None):
        if not request.data.__contains__('file') or len(request.data.__getitem__('file')) <= 0:
            return response.Response({'Error': "File not found, please upload CSV file"}, status="400")

        file_obj = request.data['file']

        # Converting file data into dictionary
        csv_file = csv.DictReader(codecs.iterdecode(file_obj, 'utf-8-sig'))
        csv_file = [dict(row) for row in csv_file]

        for row in csv_file:

            # Get or Create (Get value or create new if not exists) for AutopsyType, TissuType and Neuro Diagnosis
            tissue_type = GetOrCreate(model_name='TissueTypes').run(tissue_type=row['tissue_type'])
            neuro_diagnosis_id = GetOrCreate(model_name='NeuropathologicalDiagnosis').run(
                neuro_diagnosis_name=row['neuro_diagnosis_id'])
            autopsy_type = GetOrCreate(model_name='AutopsyTypes').run(autopsy_type=row['autopsy_type'])

            # If prime_details data is validated then save it else return error response
            prime_details = PrimeDetailsTemplate(
                mbtb_code=row['mbtb_code'], sex=row['sex'], age=row['age'],
                postmortem_interval=row['postmortem_interval'], time_in_fix=row['time_in_fix'],
                clinical_diagnosis=row['clinical_diagnosis'], tissue_type=tissue_type.tissue_type_id,
                preservation_method=row['preservation_method'],
                neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id,
                storage_year=row['storage_year'])
            prime_details_serializer = FileUploadPrimeDetailsSerializer(data=prime_details.__dict__)

            if prime_details_serializer.is_valid():
                prime_details_serializer.save()  # Saving prime_details

                # If other_details data is validated then save it else return error response
                other_details = OtherDetailsTemplate(
                    prime_details_id=prime_details_serializer.data['prime_details_id'], race=row['race'],
                    duration=row['duration'], clinical_details=row['clinical_details'],
                    cause_of_death=row['cause_of_death'], brain_weight=row['brain_weight'],
                    neuropathology_summary=row['neuropathology_summary'],
                    neuropathology_gross=row['neuropathology_gross'],
                    neuropathology_microscopic=row['neuropathology_microscopic'], cerad=row['cerad'],
                    braak_stage=row['braak_stage'], khachaturian=row['khachaturian'], abc=row['abc'],
                    autopsy_type=autopsy_type.autopsy_type_id, formalin_fixed=row['formalin_fixed'],
                    fresh_frozen=row['fresh_frozen']
                )
                other_details_serializer = FileUploadOtherDetailsSerializer(data=other_details.__dict__)
                if other_details_serializer.is_valid():
                    other_details_serializer.save()  # Saving other_details
                else:
                    # TODO: log errors here related to file data uploading for other details
                    # Return error response if any error in other_details data
                    return response.Response({
                        'Response': 'Failure',
                        'Message': 'Error in other details, Data uploading failed at mbtb_code: {}'.format(
                            row['mbtb_code']), 'Error': other_details_serializer.errors},
                        status="400")

            else:
                # TODO: log errors here related to file data uploading for prime details
                # Return error response if any error in prime_details data
                return response.Response({
                    'Response': 'Failure',
                    'Message': 'Error in other details, Data uploading failed at mbtb_code: {}'.format(
                        row['mbtb_code'])},
                    status="400")

        # Return response: data is uploaded successfully
        return response.Response({'Response': 'Success'}, status="201")
