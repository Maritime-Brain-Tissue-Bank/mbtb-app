from ..models import OtherDetails
from ..serializers import OtherDetailsSerializer


# This class is download filtered mbtb data based on given mbtb_code as a list of dict.
# It doesn't include prime_details_id, other_details_id.
class DownloadFilteredData(object):

    def __init__(self):
        pass

    def run(self, **kwargs):
        _mbtb_code_list = kwargs.get('input_mbtb_codes', None)
        _other_details_response = OtherDetails.objects.filter(
            prime_details_id__mbtb_code__in=_mbtb_code_list).select_related()
        _serializer_response = OtherDetailsSerializer(_other_details_response, many=True)

        # Converting OrderedDict to list of Dict
        _serializer_response = [dict(elem) for elem in _serializer_response.data]

        if (len(_serializer_response) is 0) or not(len(_serializer_response) == len(_mbtb_code_list)):
            return {'response': False}

        # Removing primary keys from data
        for elem in _serializer_response:
            del elem['prime_details_id']
            del elem['other_details_id']

        return {'response': True, 'data': _serializer_response}
