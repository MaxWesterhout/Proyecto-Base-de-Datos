# Generated by Django 4.2.2 on 2023-07-07 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenis', '0012_alter_match_match_num_alter_playermatchstats_result_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ranking',
            unique_together=set(),
        ),
    ]
