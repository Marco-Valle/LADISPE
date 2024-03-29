# Generated by Django 4.0.3 on 2023-02-23 14:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ladicontent', '0003_alter_ladigallery_title_alter_ladinews_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ladistaff',
            name='id',
        ),
        migrations.AlterField(
            model_name='ladistaff',
            name='user',
            field=models.OneToOneField(help_text='If you create a LADIStaff with a particular user, his name, surname and email will be public', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
