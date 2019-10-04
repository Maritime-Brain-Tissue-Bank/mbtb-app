from django.db import models


class UsersAccount(models.Model):
    email = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'
        managed = False
