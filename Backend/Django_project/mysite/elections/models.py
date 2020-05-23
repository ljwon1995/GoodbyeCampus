from django.db import models

# Create your models here.
class Substitute(models.Model):
    course_id = models.CharField(max_length=20)
    course_title = models.CharField(max_length=20)
    
    sub_id = models.CharField(max_length=20)
    sub_title = models.CharField(max_length=20)

    def __str__(self):
        return self.course_title + ':' + self.sub_title 

class Compulsory(models.Model):
    course_year = models.CharField(max_length=10)
    course_id = models.CharField(max_length=20)
    course_title = models.CharField(max_length=20)

    def __str__(self):
        return self.course_year + ':' + self.course_title

class Subject(models.Model):
    course_year = models.CharField(max_length=10)
    course_semester = models.CharField(max_length=10)
    course_colgnm = models.CharField(max_length=40)
    course_sustnm = models.CharField(max_length=40)
    course_pobjnm = models.CharField(max_length=40)
    course_shyr = models.CharField(max_length=20)
    course_profnm = models.CharField(max_length=40)
    course_ltbdrm = models.CharField(max_length=20)
    course_sbjtclss = models.CharField(max_length=40)
    course_clssnm = models.CharField(max_length=40)
    course_pnt = models.CharField(max_length=20)
    course_remk = models.CharField(max_length=50)


    def __str__(self):
        return self.course_year + ":" + self.course_semester + ":" + self.course_clssnm
