from django.db import models


class NewUsers(models.Model):
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organization = models.TextField()
    department = models.TextField()
    current_position = models.CharField(max_length=20)

    class Meta:
        db_table = 'new_users'

    def __str__(self):
        return str(self.email)


class NewUsersInfo(models.Model):
    new_users = models.ForeignKey(NewUsers, related_name='new_users_info', on_delete=models.CASCADE)
    address_line_1 = models.TextField()
    address_line_2 = models.TextField()
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    comments = models.TextField()

    class Meta:
        db_table = 'new_users_info'
