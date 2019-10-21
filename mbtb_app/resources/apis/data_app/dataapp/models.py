# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AutopsyType(models.Model):
    autopsy_type_id = models.AutoField(primary_key=True)
    autopsy_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'autopsy_type'


class BrainDataset(models.Model):
    id = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=6, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    postmortem_interval = models.CharField(max_length=255, blank=True, null=True)
    time_in_fix = models.CharField(max_length=255, blank=True, null=True)
    neuro_diseases = models.ForeignKey('NeurodegenerativeDiseases', models.DO_NOTHING)
    tissue_type = models.ForeignKey('TissueType', models.DO_NOTHING)
    storage_method = models.CharField(max_length=9, blank=True, null=True)
    storage_year = models.DateTimeField()
    archive = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brain_dataset'


class DatasetOthrDetails(models.Model):
    id = models.AutoField(primary_key=True)
    # id = models.ForeignKey(BrainDataset, models.DO_NOTHING, db_column='id')
    race = models.CharField(max_length=255, blank=True, null=True)
    diagnosis_of_dementia = models.CharField(max_length=255, blank=True, null=True)
    duration_of_dementia = models.IntegerField(blank=True, null=True)
    clinical_history = models.CharField(max_length=255, blank=True, null=True)
    cause_of_death = models.CharField(max_length=255, blank=True, null=True)
    brain_weight = models.IntegerField(blank=True, null=True)
    neoropathology_detailed = models.TextField(blank=True, null=True)
    neuropathology_gross = models.TextField(blank=True, null=True)
    neuropathology_micro = models.TextField(blank=True, null=True)
    neouropathology_criteria = models.CharField(max_length=255, blank=True, null=True)
    cerad = models.CharField(max_length=255, blank=True, null=True)
    braak_stage = models.CharField(max_length=255, blank=True, null=True)
    khachaturian = models.CharField(max_length=255, blank=True, null=True)
    abc = models.CharField(max_length=255, blank=True, null=True)
    autopsy_type = models.ForeignKey(AutopsyType, models.DO_NOTHING)
    tissue_type_formalin_fixed = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dataset_othr_details'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ImageRepository(models.Model):
    image_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(BrainDataset, models.DO_NOTHING, db_column='id')
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


class TissueType(models.Model):
    tissue_type_id = models.AutoField(primary_key=True)
    tissue_type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tissue_type'
