from django.db import models


class AdminAccount(models.Model):
    email = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=50)

    class Meta:
        db_table = 'admins'
