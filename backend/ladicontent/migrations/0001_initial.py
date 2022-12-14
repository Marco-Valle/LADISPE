# Generated by Django 4.0.3 on 2022-08-03 18:48

from django.db import migrations, models
import django.db.models.deletion
import filebrowser.fields
import phonenumber_field.modelfields
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LADIForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, unique=True)),
                ('file', models.FileField(upload_to='forms/')),
                ('public', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LADIGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LADINews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('cover', models.ImageField(default='default.png', upload_to='news/%Y/%m/%d/')),
                ('title', models.CharField(max_length=30)),
                ('link', models.URLField(blank=True, null=True)),
                ('in_evidence', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, help_text='Use &lt;br&gt; to break the line')),
            ],
            options={
                'verbose_name_plural': 'Ladi news',
            },
        ),
        migrations.CreateModel(
            name='LADIPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(upload_to='gallery/%Y/%m/%d/')),
                ('link', models.URLField(blank=True, help_text='Link to be redirected on click', null=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LADIStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(default='default.png', upload_to='staff/%Y/%m/%d/')),
                ('position', models.CharField(max_length=30)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
            ],
        ),
        migrations.CreateModel(
            name='LADIStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50)),
                ('type', models.IntegerField(choices=[(1, 'Story'), (2, 'Material')], default=1)),
                ('cover', filebrowser.fields.FileBrowseField(default='default.png', max_length=200, verbose_name='Image')),
                ('html', tinymce.models.HTMLField(blank=True)),
                ('preview', models.TextField(blank=True)),
                ('author', models.CharField(blank=True, max_length=30)),
                ('quote', models.CharField(blank=True, max_length=30)),
                ('gallery', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ladicontent.ladigallery')),
            ],
        ),
    ]
