# Generated by Django 3.2.20 on 2023-08-14 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0003_delete_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.FileField(upload_to='image'),
        ),
    ]
