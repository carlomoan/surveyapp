# Generated by Django 2.2.3 on 2021-01-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
