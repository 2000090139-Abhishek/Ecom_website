# Generated by Django 5.0.3 on 2024-03-21 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_website', '0002_alter_product_img_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(upload_to=''),
        ),
    ]
