# Generated by Django 3.1.4 on 2021-03-17 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20210315_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentstatus',
            name='accepted',
            field=models.BooleanField(db_index=True, null=True, verbose_name='Diterima'),
        ),
    ]
