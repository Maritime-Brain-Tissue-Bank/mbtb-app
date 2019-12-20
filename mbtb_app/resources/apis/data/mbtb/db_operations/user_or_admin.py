from ..models import AdminAccount, UserAccount


# This class is to fetch rows from admin and user tables
# If found, return true else false
class UserOrAdmin(object):

    def __init__(self, **kwargs):
        self.model_name = kwargs.get('model_name', None)
        self.models = {
            'User': UserAccount,
            'Admin': AdminAccount
        }

    def run(self, **kwargs):
        try:
            model_object = self.models[self.model_name].objects.get(**kwargs)  # model_object is for future reference
            return True

        except self.models[self.model_name].DoesNotExist:
            return False
