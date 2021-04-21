# Generated by Django 2.1 on 2020-08-11 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=100)),
                ('dept', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=100)),
                ('comp_profile', models.CharField(max_length=100)),
                ('ctc', models.IntegerField()),
                ('eligibility', models.FloatField()),
                ('bond', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('venue', models.TextField(max_length=200)),
                ('branch', models.CharField(max_length=100)),
                ('instruction', models.CharField(max_length=200)),
                ('campus', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='resetPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=200)),
                ('time', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('getTime', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentPlaced',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stud_name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('id_no', models.IntegerField()),
                ('ctc', models.IntegerField()),
                ('stud_user', models.CharField(max_length=100)),
                ('comp_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StudentsEligible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stud_name', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('stud_user', models.CharField(max_length=100)),
                ('comp_name', models.CharField(max_length=100)),
            ],
        ),
    ]
