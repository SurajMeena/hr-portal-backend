# Generated by Django 5.0.7 on 2024-08-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='start_date',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.CharField(choices=[('Manager', 'Manager'), ('Developer', 'Developer'), ('Designer', 'Designer'), ('Analyst', 'Analyst'), ('Intern', 'Intern'), ('HR', 'HR')], max_length=50),
        ),
    ]
