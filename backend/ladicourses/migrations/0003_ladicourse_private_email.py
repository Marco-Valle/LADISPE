# Generated by Django 4.0.3 on 2023-02-23 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ladicourses', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ladicourse',
            name='private_email',
            field=models.BooleanField(default=False),
        ),
    ]
