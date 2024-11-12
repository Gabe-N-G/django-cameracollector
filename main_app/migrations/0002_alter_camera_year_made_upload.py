# Generated by Django 5.1.3 on 2024-11-12 23:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='year_made',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('process', models.CharField(choices=[('UPL', 'Upload'), ('DEV', 'Develop'), ('SCN', 'Scan'), ('PRT', 'Print')], default='UPL', max_length=3)),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.camera')),
            ],
        ),
    ]
