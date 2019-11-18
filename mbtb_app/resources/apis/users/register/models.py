from django.db import models


class Users(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    institution = models.TextField()
    department_name = models.TextField()
    position_title = models.CharField(max_length=30)
    address_line_1 = models.TextField(blank=True)
    address_line_2 = models.TextField(blank=True)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10, blank=True)
    comments = models.TextField(blank=True)
    pending_approval = models.CharField(max_length=1, default='Y')
    active_since = models.DateField(auto_now_add=True)

    class Meta:
        #managed = False
        db_table = 'users'
