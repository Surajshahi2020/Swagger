# Generated by Django 4.2 on 2023-04-17 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
