# Generated by Django 5.0.6 on 2024-07-11 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_alter_watch_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='platform',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='app1.streamingplatform'),
            preserve_default=False,
        ),
    ]
