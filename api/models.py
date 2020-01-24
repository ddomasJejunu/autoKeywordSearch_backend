from django.db import models

# Create your models here.
class User(models.Model):
    no = models.AutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=20)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

class Keywordsearch(models.Model):
    no = models.AutoField(primary_key=True)
    search_url = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    user_no = models.ForeignKey('User', models.DO_NOTHING, db_column='user_no')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    complete_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywordsearch'