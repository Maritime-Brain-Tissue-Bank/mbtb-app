from ..models import OtherDetails
from ..serializers import OtherDetailsSerializer


# This class is to download all mbtb data without prime_details_id, other_details_id as a list of dict
class DownloadAllData(object):

    def __init__(self):
        pass

    def run(self):
        _other_details_response = OtherDetails.objects.all().select_related()
        _serializer_response = OtherDetailsSerializer(_other_details_response, many=True)

        # Converting OrderedDict to list of list
        _serializer_response = [dict(elem) for elem in _serializer_response.data]

        if (len(_serializer_response) is 0):
            return {'response': False}

        # Removing primary keys from data
        for elem in _serializer_response:
            del elem['prime_details_id']
            del elem['other_details_id']

        return {'response': True, 'data': _serializer_response}
