# Generated by Django 5.1.1 on 2024-10-13 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
