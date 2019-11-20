from django.db import models
from datetime import datetime


class AutopsyType(models.Model):
    autopsy_type_id = models.AutoField(primary_key=True)
    autopsy_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'autopsy_type'

    def __str__(self):
        return self.autopsy_type


class BrainDataset(models.Model):
    brain_data_id = models.AutoField(primary_key=True)
    mbtb_code = models.CharField(max_length=50)
    sex = models.CharField(max_length=6, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    postmortem_interval = models.CharField(max_length=255, blank=True, null=True)
    time_in_fix = models.CharField(max_length=255, blank=True, null=True)
    neuro_diseases_id = models.ForeignKey('NeurodegenerativeDiseases', models.DO_NOTHING, db_column="neuro_diseases_id")
    tissue_type = models.ForeignKey('TissueType', models.DO_NOTHING)
    storage_method = models.CharField(max_length=20, blank=True, null=True)
    storage_year = models.DateTimeField(default=datetime.now, blank=True)
    archive = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brain_dataset'

    def __str__(self):
        return self.mbtb_code


class DatasetOthrDetails(models.Model):
    othr_details_id = models.AutoField(primary_key=True)
    brain_data_id = models.ForeignKey(BrainDataset, models.DO_NOTHING, db_column="brain_data_id")
    race = models.CharField(max_length=255, blank=True, null=True)
    diagnosis = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    clinical_history = models.CharField(max_length=255, blank=True, null=True)
    cause_of_death = models.CharField(max_length=255, blank=True, null=True)
    brain_weight = models.IntegerField(blank=True, null=True)
    neuoropathology_detailed = models.TextField(blank=True, null=True)
    neuropathology_gross = models.TextField(blank=True, null=True)
    neuropathology_micro = models.TextField(blank=True, null=True)
    neouropathology_criteria = models.CharField(max_length=255, blank=True, null=True)
    cerad = models.CharField(max_length=255, blank=True, null=True)
    braak_stage = models.CharField(max_length=255, blank=True, null=True)
    khachaturian = models.CharField(max_length=255, blank=True, null=True)
    abc = models.CharField(max_length=255, blank=True, null=True)
    autopsy_type = models.ForeignKey(AutopsyType, models.DO_NOTHING)
    formalin_fixed = models.CharField(max_length=5, blank=True, null=True)
    fresh_frozen = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_othr_details'


class ImageRepository(models.Model):
    image_id = models.AutoField(primary_key=True)
    brain_data_id = models.ForeignKey(BrainDataset, models.DO_NOTHING, db_column="brain_data_id")
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


class NeurodegenerativeDiseases(models.Model):
    neuro_diseases_id = models.AutoField(primary_key=True)
    disease_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'neurodegenerative_diseases'

    def __str__(self):
        return self.disease_name


class TissueType(models.Model):
    tissue_type_id = models.AutoField(primary_key=True)
    tissue_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tissue_type'

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
