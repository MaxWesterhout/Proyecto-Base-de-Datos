# Generated by Django 4.2.2 on 2023-06-30 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenis', '0008_remove_playermatchstats_score_match_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='id',
            field=models.CharField(max_length=16, primary_key=True, serialize=False),
        ),
    ]
