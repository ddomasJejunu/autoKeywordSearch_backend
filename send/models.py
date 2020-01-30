from django.db import models

# Create your models here.
class User(models.Model):
    no = models.AutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=20)
    email = models.CharField(max_length=255, blank=True, null=True)
    device_id = models.CharField(unique=True, max_length=16, blank=True, null=True)
    platform = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'