# Generated by Django 5.0.3 on 2024-03-21 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
