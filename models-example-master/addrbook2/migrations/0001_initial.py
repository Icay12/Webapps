# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-13 15:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=20)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('state', models.CharField(blank=True, max_length=20)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('country', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=32)),
                ('home_phone', models.CharField(blank=True, max_length=16)),
                ('cell_phone', models.CharField(blank=True, max_length=16)),
                ('fax', models.CharField(blank=True, max_length=16)),
                ('spouse_last', models.CharField(blank=True, max_length=16)),
                ('spouse_first', models.CharField(blank=True, max_length=16)),
                ('spouse_birth', models.DateField(blank=True, null=True)),
                ('spouse_cell', models.CharField(blank=True, max_length=16)),
                ('spouse_email', models.CharField(blank=True, max_length=32)),
                ('creation_time', models.DateTimeField()),
                ('update_time', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_creators', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_updators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
