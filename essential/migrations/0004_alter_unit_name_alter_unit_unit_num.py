# Generated by Django 5.1.4 on 2024-12-08 18:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("essential", "0003_alter_book_level_alter_book_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unit",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="unit",
            name="unit_num",
            field=models.PositiveIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(2),
                ],
            ),
        ),
    ]
