# Generated by Django 3.2.2 on 2021-05-12 19:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20210512_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=155)),
                ('landmark', models.CharField(max_length=55)),
                ('pincode', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{6}$')])),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.CharField(blank=True, choices=[('1', 'Pending'), ('2', 'Aproved'), ('3', 'Rejected')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='aadhar_number',
            field=models.CharField(default=1, max_length=12, validators=[django.core.validators.RegexValidator(message='Aadhar number must be entered only 12 digits allowed.', regex='^\\+?1?\\d{12}$')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=phone_field.models.PhoneField(help_text='Contact phone number', max_length=31),
        ),
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.address'),
        ),
        migrations.AddField(
            model_name='vendor',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.address'),
        ),
    ]
