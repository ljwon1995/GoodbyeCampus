# parsed_data/models.py
from django.db import models


class BlogData(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
    	return self.title

class Subject(models.Model):
    year = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    credit = models.CharField(max_length=10)
    etc = models.CharField(max_length=200)

    def __str__(self):
        return self.year+' '+self.code+' '+self.title


