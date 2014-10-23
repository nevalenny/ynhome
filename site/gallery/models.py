from django.db import models

# Create your models here.

class Picture(models.Model):
	"""all necessary data for Picture"""
	title = models.CharField(max_length=200)
	taken_date = models.DateTimeField('date taken')
	url = models.CharField(max_length=200)


