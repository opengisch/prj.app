# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0019_auto_20180420_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='certifyingorganisation',
            name='description',
            field=models.TextField(help_text='Description of Organisation or Institution and it contributes to the project.', max_length=3000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='address',
            field=models.TextField(help_text='Address of Organisation or Institution.'),
        ),
    ]
