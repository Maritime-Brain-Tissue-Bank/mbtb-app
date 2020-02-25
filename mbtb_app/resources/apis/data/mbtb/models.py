from django.db import models
from datetime import datetime


class AutopsyTypes(models.Model):
    autopsy_type_id = models.AutoField(primary_key=True)
    autopsy_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'autopsy_types'

    def __str__(self):
        return self.autopsy_type


class PrimeDetails(models.Model):
    prime_details_id = models.AutoField(primary_key=True)
    mbtb_code = models.CharField(max_length=50, unique=True)
    sex = models.CharField(max_length=6, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    postmortem_interval = models.CharField(max_length=255, blank=True, null=True)
    time_in_fix = models.CharField(max_length=255, blank=True, null=True)
    clinical_diagnosis = models.CharField(max_length=255, blank=True, null=True)
    tissue_type = models.ForeignKey('TissueTypes', models.DO_NOTHING)
    preservation_method = models.CharField(max_length=20, blank=True, null=True)
    storage_year = models.DateTimeField(default=datetime.now, blank=True)
    archive = models.CharField(max_length=3, blank=True, null=True)
    neuro_diagnosis_id = models.ForeignKey('NeuropathologicalDiagnosis', models.DO_NOTHING,
                                           db_column="neuro_diagnosis_id")

    class Meta:
        managed = False
        db_table = 'prime_details'

    def __str__(self):
        return self.mbtb_code


class OtherDetails(models.Model):
    other_details_id = models.AutoField(primary_key=True)
    prime_details_id = models.ForeignKey(PrimeDetails, models.DO_NOTHING, db_column="prime_details_id")
    race = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    clinical_details = models.TextField(blank=True, null=True)
    cause_of_death = models.CharField(max_length=255, blank=True, null=True)
    brain_weight = models.IntegerField(blank=True, null=True)
    neuropathology_summary = models.TextField(blank=True, null=True)
    neuropathology_gross = models.TextField(blank=True, null=True)
    neuropathology_microscopic = models.TextField(blank=True, null=True)
    neouropathology_criteria = models.CharField(max_length=255, blank=True, null=True)
    cerad = models.CharField(max_length=255, blank=True, null=True)
    braak_stage = models.CharField(max_length=255, blank=True, null=True)
    khachaturian = models.CharField(max_length=255, blank=True, null=True)
    abc = models.CharField(max_length=255, blank=True, null=True)
    autopsy_type = models.ForeignKey(AutopsyTypes, models.DO_NOTHING)
    formalin_fixed = models.CharField(max_length=5, blank=True, null=True)
    fresh_frozen = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_details'


class ImageRepository(models.Model):
    image_id = models.AutoField(primary_key=True)
    prime_details_id = models.ForeignKey(PrimeDetails, models.DO_NOTHING, db_column="prime_details_id")
    file_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_type = models.CharField(max_length=255)
    file_size = models.IntegerField()
    category = models.CharField(max_length=7, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date_taken = models.DateField(blank=True, null=True)
    date_inserted = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'image_repository'


class NeuropathologicalDiagnosis(models.Model):
    neuro_diagnosis_id = models.AutoField(primary_key=True)
    neuro_diagnosis_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'neuropathological_diagnosis'

    def __str__(self):
        return self.neuro_diagnosis_name


class TissueTypes(models.Model):
    tissue_type_id = models.AutoField(primary_key=True)
    tissue_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tissue_types'

    def __str__(self):
        return self.tissue_type


class AdminAccount(models.Model):
    email = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'admins'


class UserAccount(models.Model):
    email = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'users'
