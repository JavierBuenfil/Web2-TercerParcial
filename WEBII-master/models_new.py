# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiUsers(models.Model):
    user = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    api_key = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_users'


class Movie(models.Model):
    movieid = models.CharField(db_column='MovieID', primary_key=True, max_length=10)  # Field name made lowercase.
    movietitle = models.CharField(db_column='MovieTitle', max_length=30)  # Field name made lowercase.
    releasedate = models.DateField(db_column='ReleaseDate')  # Field name made lowercase.
    genereid = models.CharField(db_column='GenereID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    directorid = models.CharField(db_column='DirectorID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageUrl', max_length=250)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'movie'
