# Generated by Django 3.1.12 on 2024-12-05 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileU', '0003_auto_20241205_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
