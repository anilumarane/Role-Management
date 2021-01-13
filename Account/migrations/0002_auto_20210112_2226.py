# Generated by Django 3.1.2 on 2021-01-12 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemaccess',
            name='is_add',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=250),
        ),
        migrations.AlterField(
            model_name='systemaccess',
            name='is_delete',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=250),
        ),
        migrations.AlterField(
            model_name='systemaccess',
            name='is_read',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=250),
        ),
        migrations.AlterField(
            model_name='systemaccess',
            name='is_update',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=250),
        ),
    ]
