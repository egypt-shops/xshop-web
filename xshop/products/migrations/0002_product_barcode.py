# Generated by Django 3.1.2 on 2020-11-15 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
    ]
