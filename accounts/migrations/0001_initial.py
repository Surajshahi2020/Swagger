# Generated by Django 4.2 on 2023-04-14 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('role', models.CharField(max_length=2)),
                ('is_active', models.BooleanField(default=True)),
                ('is_blocked', models.BooleanField(default=True)),
            ],
        ),
    ]
