# Generated by Django 4.1.5 on 2023-06-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_products_star'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='star',
            field=models.IntegerField(blank=True, default=2),
        ),
    ]