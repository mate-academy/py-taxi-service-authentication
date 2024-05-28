# Generated by Django 4.1 on 2024-05-28 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxi', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='driver',
            name='license_number',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
