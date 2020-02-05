from django.db import models


class TissueRequests(models.Model):
    tissue_requests_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    institution = models.TextField()
    department_name = models.TextField()
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, blank=True)
    fax_number = models.CharField(max_length=20, blank=True)
    project_title = models.TextField()
    source_of_funding = models.TextField()
    abstract = models.TextField()
    pending_approval = models.CharField(max_length=1, default='Y')

    class Meta:
        managed = False
        db_table = 'tissue_requests'

    def __str__(self):
        return self.tissue_requests_id
