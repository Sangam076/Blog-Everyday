# Generated by Django 5.1.4 on 2024-12-29 15:15

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_alter_blogpost_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=tinymce.models.HTMLField(),
        ),
    ]
