import codecs
import csv
import json

from rest_framework import viewsets, views, response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .data_templates.other_details import OtherDetailsTemplate
from .data_templates.prime_details import PrimeDetailsTemplate
from .db_operations.get_or_create import GetOrCreate
from .db_operations.download_all_data import DownloadAllData
from .db_operations.download_filtered_data import DownloadFilteredData
from .models import AutopsyTypes, PrimeDetails, OtherDetails, NeuropathologicalDiagnosis, \
    TissueTypes
from .serializers import PrimeDetailsSerializer, OtherDetailsSerializer, FileUploadPrimeDetailsSerializer, \
    FileUploadOtherDetailsSerializer, InsertRowPrimeDetailsSerializer
from .validations.validate_data import ValidateData
from .permissions.is_authenticated import IsAuthenticated
from .permissions.is_admin import IsAdmin


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
    permission_classes = [IsAdmin]

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
            prime_serializer_instance = prime_details_serializer.save()  # Saving prime_details

            # If other_details data is validated then save it else return error response
            _duration = validate_data.check_is_number(value=request.data['duration'])
            _brain_weight = validate_data.check_is_number(value=request.data['brain_weight'])

            if (not _duration['Response']) or (not _brain_weight['Response']):
                return response.Response({'Error': 'Expecting value, received text for duration and/or brain_weight.'},
                                         status="400")

            other_details = OtherDetailsTemplate(
                prime_details_id=prime_details_serializer.data['prime_details_id'], race=request.data['race'],
                duration=_duration['Value'], clinical_details=request.data['clinical_details'],
                cause_of_death=request.data['cause_of_death'], brain_weight=_brain_weight['Value'],
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

                # deleting instance if any error in other_details data
                prime_serializer_instance.delete()

                # Return error response if any error in other_details data
                return response.Response(
                    {'Error': 'Error in other_details, Inserting data failed.'},
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


# This view class is to upload and edit data via csv file in prime_details, other_details, allowed methods: POST, PATCH
class FileUploadAPIView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdmin]

    # For `POST` request: upload data via csv file
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
            _preservation_method = validate_data.check_preservation_method(
                formalin_fixed=row['formalin_fixed'], fresh_frozen=row['fresh_frozen']
            )
            prime_details = PrimeDetailsTemplate(
                mbtb_code=row['mbtb_code'], sex=row['sex'], age=row['age'],
                postmortem_interval=row['postmortem_interval'], time_in_fix=row['time_in_fix'],
                clinical_diagnosis=row['clinical_diagnosis'], tissue_type=tissue_type.tissue_type_id,
                preservation_method=_preservation_method,
                neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id,
                storage_year=row['storage_year']
            )
            prime_details_serializer = FileUploadPrimeDetailsSerializer(data=prime_details.__dict__)

            if prime_details_serializer.is_valid():
                prime_serializer_instance = prime_details_serializer.save()  # Saving prime_details

                # If other_details data is validated then save it else return error response
                _duration = validate_data.check_is_number(value=row['duration'])
                _brain_weight = validate_data.check_is_number(value=row['brain_weight'])

                if (not _duration['Response']) or (not _brain_weight['Response']):
                    _error = 'Expecting value, received text for duration and/or brain_weight at mbtb_code: {}.' \
                        .format(row['mbtb_code'])
                    return response.Response({'Error': _error}, status="400")

                # If other_details data is validated then save it else return error response
                other_details = OtherDetailsTemplate(
                    prime_details_id=prime_details_serializer.data['prime_details_id'], race=row['race'],
                    duration=_duration['Value'], clinical_details=row['clinical_details'],
                    cause_of_death=row['cause_of_death'], brain_weight=_brain_weight['Value'],
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

                    # deleting instance if any error in other_details data
                    prime_serializer_instance.delete()

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

    # For `PATCH` request: edit data via csv file
    def patch(self, request, format=None):
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

            # Get prime_details, other_details based on prime_details_id or return 404 if not found
            prime_details = get_object_or_404(PrimeDetails, mbtb_code=row['mbtb_code'])
            other_details = get_object_or_404(OtherDetails, prime_details_id=prime_details.prime_details_id)

            # Get or Create (Get value or create new if not exists) for AutopsyType, TissuType and Neuro Diagnosis
            tissue_type = GetOrCreate(model_name='TissueTypes').run(tissue_type=row['tissue_type'])
            neuro_diagnosis_id = GetOrCreate(model_name='NeuropathologicalDiagnosis').run(
                neuro_diagnosis_name=row['neuropathology_diagnosis'])
            autopsy_type = GetOrCreate(model_name='AutopsyTypes').run(autopsy_type=row['autopsy_type'])

            # If prime_details data is validated then save it else return error response
            _preservation_method = validate_data.check_preservation_method(
                formalin_fixed=row['formalin_fixed'], fresh_frozen=row['fresh_frozen']
            )
            prime_details_template_data = PrimeDetailsTemplate(
                mbtb_code=row['mbtb_code'], sex=row['sex'], age=row['age'],
                postmortem_interval=row['postmortem_interval'], time_in_fix=row['time_in_fix'],
                clinical_diagnosis=row['clinical_diagnosis'], tissue_type=tissue_type.tissue_type_id,
                preservation_method=_preservation_method,
                neuro_diagnosis_id=neuro_diagnosis_id.neuro_diagnosis_id,
                storage_year=row['storage_year']
            )
            prime_details_serializer = FileUploadPrimeDetailsSerializer(
                prime_details, data=prime_details_template_data.__dict__, partial=True
            )

            if prime_details_serializer.is_valid():
                prime_details_serializer.save()  # Saving prime_details

                # If other_details data is validated then save it else return error response
                _duration = validate_data.check_is_number(value=row['duration'])
                _brain_weight = validate_data.check_is_number(value=row['brain_weight'])

                if (not _duration['Response']) or (not _brain_weight['Response']):
                    _error = 'Expecting value, received text for duration and/or brain_weight at mbtb_code: {}.' \
                        .format(row['mbtb_code'])
                    return response.Response({'Error': _error}, status="400")

                # If other_details data is validated then save it else return error response
                other_details_template_data = OtherDetailsTemplate(
                    prime_details_id=prime_details.prime_details_id, race=row['race'],
                    duration=_duration['Value'], clinical_details=row['clinical_details'],
                    cause_of_death=row['cause_of_death'], brain_weight=_brain_weight['Value'],
                    neuropathology_summary=row['neuropathology_summary'],
                    neuropathology_gross=row['neuropathology_gross'],
                    neuropathology_microscopic=row['neuropathology_microscopic'], cerad=row['cerad'],
                    braak_stage=row['braak_stage'], khachaturian=row['khachaturian'], abc=row['abc'],
                    autopsy_type=autopsy_type.autopsy_type_id, formalin_fixed=row['formalin_fixed'],
                    fresh_frozen=row['fresh_frozen']
                )
                other_details_serializer = FileUploadOtherDetailsSerializer(
                    other_details, data=other_details_template_data.__dict__, partial=True
                )
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


# This view class allows us to edit single row of mbtb_data: prime_details, other_details, allowed methods: PATCH
class EditDataAPIView(views.APIView):
    permission_classes = [IsAdmin]

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
            _duration = validate_data.check_is_number(value=request.data['duration'])
            _brain_weight = validate_data.check_is_number(value=request.data['brain_weight'])

            if (not _duration['Response']) or (not _brain_weight['Response']):
                return response.Response({'Error': 'Expecting value, received text for duration and/or brain_weight.'},
                                         status="400")

            other_details_template_data = OtherDetailsTemplate(
                prime_details_id=prime_details_id, race=request.data['race'],
                duration=_duration['Value'], clinical_details=request.data['clinical_details'],
                cause_of_death=request.data['cause_of_death'], brain_weight=_brain_weight['Value'],
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


# This view class allows us to delete data from mbtb_data: prime_details, other_details, allowed_methods: DELETE
class DeleteDataAPIView(views.APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, prime_details_id, format=None):
        # Get prime_details instance with prime_details_id, return 404 if not found, then delete it
        prime_details = get_object_or_404(PrimeDetails, prime_details_id=prime_details_id)
        other_details = get_object_or_404(OtherDetails, prime_details_id=prime_details_id)
        other_details.delete()
        prime_details.delete()
        return response.Response({'Response': 'Success'}, status="200")  # Return response


# This view class fetches mbtb_data based on given multiple mbtb_code values in input, allowed_methods: POST
class DownloadDataAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # validate request data for 'download_mode' tag
        if not ("download_mode" in request.data):
            return response.Response({"Error": "Please provide data with 'download_mdoe' tag"}, status="400")

        _download_mode = request.data["download_mode"]

        if _download_mode == "all":
            download_all_data = DownloadAllData()
            _response = download_all_data.run()

            if not _response['response']:
                return response.Response({
                    "Error": "Something went wrong, please try again!"}, status="400")

            return response.Response(_response["data"], status="200")

        elif _download_mode == "filtered":
            # validate request data for 'download_data' tag
            if not ("download_data" in request.data):
                return response.Response({'Error': "Please provide data with 'download_data' tag"}, status="400")

            _received_input = request.data["download_data"]

            # Converting list of dict i.e _received_input to list containing received keys
            # For checking 'mbtb_code' is present or not.
            # Finally, validating with 'mbtb_code' tag and its length, return error if any of it doesn't follow.
            _received_keys = list(set().union(*(i.keys() for i in _received_input)))
            if not ('mbtb_code' in _received_keys) or not (len(_received_keys) is 1):
                return response.Response(
                    {'Error': "'mbtb_code' not found, Please provide values with it."}, status="400"
                )
            _mbtb_code_list = [elem['mbtb_code'] for elem in _received_input]
            download_filtered_data = DownloadFilteredData()
            _response = download_filtered_data.run(input_mbtb_codes=_mbtb_code_list)

            if not _response['response']:
                return response.Response({
                    "Error": "Invalid mbtb_code present, data not found"}, status="400")

            return response.Response(_response["data"], status="200")

        else:
            return response.Response({
                "Error": "Invalid download_mode option, allowed options are 'all', 'filtered'."}, status="400")
