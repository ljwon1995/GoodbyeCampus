# Generated by Django 3.0.5 on 2020-05-20 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0008_subject'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subject',
        ),
    ]