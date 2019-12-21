# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-21 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paintings', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(blank=True, default='', max_length=128)),
                ('address_line2', models.CharField(blank=True, default='', max_length=128)),
                ('city', models.CharField(blank=True, default='', max_length=64)),
                ('county', models.CharField(blank=True, default='', max_length=64)),
                ('country', models.CharField(blank=True, default='', max_length=64)),
                ('zip_code', models.CharField(blank=True, default='', max_length=8)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkout.Order')),
                ('painting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paintings.Painting')),
            ],
        ),
    ]
