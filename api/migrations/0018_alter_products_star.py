# Generated by Django 4.1.5 on 2023-06-01 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_myuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='star',
            field=models.IntegerField(blank=True),
        ),
    ]
