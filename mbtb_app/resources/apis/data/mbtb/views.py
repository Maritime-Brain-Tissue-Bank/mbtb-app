import codecs
import csv

from rest_framework import viewsets, views, response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .data_templates.other_details import OtherDetailsTemplate
from .data_templates.prime_details import PrimeDetailsTemplate
from .db_operations.get_or_create import GetOrCreate
from .permissions import IsAuthenticated
from .models import AutopsyTypes, PrimeDetails, OtherDetails, NeuropathologicalDiagnosis, \
    TissueTypes
from .serializers import PrimeDetailsSerializer, OtherDetailsSerializer, FileUploadPrimeDetailsSerializer, \
    FileUploadOtherDetailsSerializer, InsertRowPrimeDetailsSerializer
from .validations.validate_data import ValidateData


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

        # Validate column names for input data
        validate_data = ValidateData()
        _column_names = validate_data.check_column_names(column_names=list(request.data.keys()))
        if not _column_names['Response']:
            return response.Response({'Error': _column_names['Message']}, status="400")

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
            neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id
        )
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
                return response.Response({'Response': 'Success'}, status="201")  # Return response

            else:
                # TODO: log errors here related to add single data for other_details
                # Return error response if any error in other_details data
                return response.Response(
                    {'Error': 'Error in other details, Inserting data failed.'},
                    status="400"
                )

        else:
            # TODO: log errors here related to add single data for prime details
            # Return error response if any error in prime_details data
            return response.Response(
                {'Error': 'Error in prime_details, Inserting data failed.'},
                status="400")


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

    def post(self, request, format=None):
        validate_data = ValidateData()
        _file_tag = validate_data.check_file_tag(request=request)  # Check for `file` tag
        if not _file_tag['Response']:
            return response.Response({'Error': _file_tag['Message']}, status="400")

        _file_obj = request.data['file']
        _file_type = validate_data.check_file_type(filename=str(_file_obj))  # Check for file type
        if not _file_type['Response']:
            return response.Response({'Error': _file_type['Message']}, status="400")

        # Converting file data into dictionary
        _csv_file = csv.DictReader(codecs.iterdecode(_file_obj, 'utf-8-sig'))
        _csv_file = [dict(row) for row in _csv_file]
        _file_size = validate_data.check_file_size(csv_file=_csv_file)  # Check file size
        if not _file_size['Response']:
            return response.Response({'Error': _file_size['Message']}, status="400")

        _column_names = validate_data.check_column_names(column_names=list(_csv_file[0].keys()))  # Check column names
        if not _column_names['Response']:
            return response.Response({'Error': _column_names['Message']}, status="400")

        for row in _csv_file:

            # Get or Create (Get value or create new if not exists) for AutopsyType, TissuType and Neuro Diagnosis
            tissue_type = GetOrCreate(model_name='TissueTypes').run(tissue_type=row['tissue_type'])
            neuro_diagnosis_id = GetOrCreate(model_name='NeuropathologicalDiagnosis').run(
                neuro_diagnosis_name=row['neuropathology_diagnosis'])
            autopsy_type = GetOrCreate(model_name='AutopsyTypes').run(autopsy_type=row['autopsy_type'])

            # If prime_details data is validated then save it else return error response
            prime_details = PrimeDetailsTemplate(
                mbtb_code=row['mbtb_code'], sex=row['sex'], age=row['age'],
                postmortem_interval=row['postmortem_interval'], time_in_fix=row['time_in_fix'],
                clinical_diagnosis=row['clinical_diagnosis'], tissue_type=tissue_type.tissue_type_id,
                preservation_method=row['preservation_method'],
                neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id,
                storage_year=row['storage_year']
            )
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
                    return response.Response(
                        {'Response': 'Failure',
                         'Message': 'Error in other details, Data uploading failed at mbtb_code: {}'.format(
                             row['mbtb_code']), 'Error': other_details_serializer.errors},
                        status="400"
                    )

            else:
                # TODO: log errors here related to file data uploading for prime details
                # Return error response if any error in prime_details data
                return response.Response(
                    {'Response': 'Failure',
                     'Message': 'Error in prime details, Data uploading failed at mbtb_code: {}'.format(
                         row['mbtb_code']), 'Error': prime_details_serializer.errors},
                    status="400"
                )

        # Return response: data is uploaded successfully
        return response.Response({'Response': 'Success'}, status="201")


class EditDataAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, prime_details_id, format=None):
        if not request.data:
            return response.Response({'Error': "Please provide mbtb data"}, status="400")

        # Validate column names
        validate_data = ValidateData()
        _column_names = validate_data.check_column_names(column_names=list(request.data.keys()))
        if not _column_names['Response']:
            return response.Response({'Error': _column_names['Message']}, status="400")

        # Get prime_details, other_details based on prime_details_id or return 404 if not found
        prime_details = get_object_or_404(PrimeDetails, prime_details_id=prime_details_id)
        other_details = get_object_or_404(OtherDetails, prime_details_id=prime_details_id)

        # Get or Create (Get value or create new if not exists) for AutopsyType, TissuType and Neuro Diagnosis
        tissue_type = GetOrCreate(model_name='TissueTypes').run(tissue_type=request.data['tissue_type'])
        neuro_diagnosis_id = GetOrCreate(model_name='NeuropathologicalDiagnosis').run(
            neuro_diagnosis_name=request.data['neuropathology_diagnosis'])
        autopsy_type = GetOrCreate(model_name='AutopsyTypes').run(autopsy_type=request.data['autopsy_type'])

        prime_details_template_data = PrimeDetailsTemplate(
            mbtb_code=request.data['mbtb_code'], sex=request.data['sex'], age=request.data['age'],
            postmortem_interval=request.data['postmortem_interval'], time_in_fix=request.data['time_in_fix'],
            clinical_diagnosis=request.data['clinical_diagnosis'], tissue_type=tissue_type.tissue_type_id,
            preservation_method=request.data['preservation_method'],
            neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id
        )
        prime_details_serializer = InsertRowPrimeDetailsSerializer(
            prime_details, data=prime_details_template_data.__dict__, partial=True
        )
        if prime_details_serializer.is_valid():
            prime_details_serializer.save()  # Saving prime_details

            # If other_details data is validated then save it else return error response
            other_details_template_data = OtherDetailsTemplate(
                prime_details_id=prime_details_id, race=request.data['race'],
                duration=request.data['duration'], clinical_details=request.data['clinical_details'],
                cause_of_death=request.data['cause_of_death'], brain_weight=request.data['brain_weight'],
                neuropathology_summary=request.data['neuropathology_summary'],
                neuropathology_gross=request.data['neuropathology_gross'],
                neuropathology_microscopic=request.data['neuropathology_microscopic'], cerad=request.data['cerad'],
                braak_stage=request.data['braak_stage'], khachaturian=request.data['khachaturian'],
                abc=request.data['abc'], autopsy_type=autopsy_type.autopsy_type_id,
                formalin_fixed=request.data['formalin_fixed'], fresh_frozen=request.data['fresh_frozen']
            )
            other_details_serializer = FileUploadOtherDetailsSerializer(
                other_details, data=other_details_template_data.__dict__, partial=True
            )
            if other_details_serializer.is_valid():
                other_details_serializer.save()  # Saving other_details
                return response.Response({'Response': 'Success'}, status="201")  # Return response

            else:
                # TODO: log errors here related to add single data for other_details
                # Return error response if any error in other_details data
                return response.Response(
                    {'Error': 'Error in other details, Uploading data failed.'},
                    status="400"
                )

        else:
            # TODO: log errors here related to add single data for prime details
            # Return error response if any error in prime_details data
            return response.Response(
                {'Error': 'Error in prime_details, Uploading data failed.'},
                status="400"
            )
