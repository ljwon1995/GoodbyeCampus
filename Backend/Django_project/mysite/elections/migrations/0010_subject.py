# Generated by Django 3.0.5 on 2020-05-20 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0009_delete_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_year', models.CharField(max_length=10)),
                ('course_semester', models.CharField(max_length=10)),
                ('course_pobjnm', models.CharField(max_length=40)),
                ('course_sbjtclss', models.CharField(max_length=40)),
                ('course_clssnm', models.CharField(max_length=40)),
                ('course_pnt', models.CharField(max_length=20)),
                ('course_remk', models.CharField(max_length=50)),
            ],
        ),
    ]
