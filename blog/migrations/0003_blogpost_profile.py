# Generated by Django 5.1.4 on 2024-12-24 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
