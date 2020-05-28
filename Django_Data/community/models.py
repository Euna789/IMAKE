from django.db import models
from django.conf import settings


# Create your models here.
class Article(models.Model):
	cdate = models.DateTimeField(auto_now_add = True)
	user_info = models.CharField(max_length = 50, default = "no-user")
	program_info = models.CharField(max_length = 50)
	user_img = models.ImageField(blank=True, upload_to = '')
	content_img = models.ImageField(blank=True, upload_to = '')
	cdate = models.DateTimeField(auto_now_add = True)
	