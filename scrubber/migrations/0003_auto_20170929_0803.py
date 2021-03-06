# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-29 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrubber', '0002_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mTurk_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('code', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='workers',
            field=models.TextField(default='[]'),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='alteredText',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='originalText',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='scrubbedText',
            field=models.TextField(blank=True),
        ),
    ]
