# Generated by Django 5.1.1 on 2024-10-13 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='roles',
            field=models.ManyToManyField(default='User', related_name='users', to='accounts.role'),
        ),
    ]
