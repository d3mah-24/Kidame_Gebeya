# Generated by Django 4.1.4 on 2023-01-22 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_products_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, height_field=225, upload_to='uploads/', width_field=225),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
    ]
