# Generated by Django 5.1.4 on 2024-12-23 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedition',
            name='stock_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
