from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
# maria db 연동 - https://lsjsj92.tistory.com/480
class User(models.Model):
    no = models.AutoField(primary_key=True)
    id = models.CharField(unique=True, max_length=20)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

class Blog(models.Model):
    no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', models.DO_NOTHING, db_column='author', blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog'

class Comment(models.Model):
    no = models.AutoField(primary_key=True)
    blog = models.ForeignKey(Blog, models.DO_NOTHING, db_column='blog', blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_user = models.TextField(max_length=20)
    comment_thumbnail_url = models.TextField(max_length=300)
    comment_textfield = models.TextField()

    class Meta:
        managed = False
        db_table = 'comment'