# Generated by Django 5.1.3 on 2024-12-04 17:27

import projectStickFit.accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_appprofile_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, validators=[projectStickFit.accounts.validators.validate_minimum_age, projectStickFit.accounts.validators.validate_maximum_age]),
        ),
    ]
