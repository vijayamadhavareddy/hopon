# Generated by Django 3.2.2 on 2021-05-12 19:37

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='email',
        ),
        migrations.AddField(
            model_name='vendor',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Pending'), ('2', 'Aproved'), ('3', 'Rejected')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, default=1, help_text='Contact phone number', max_length=31),
            preserve_default=False,
        ),
    ]
