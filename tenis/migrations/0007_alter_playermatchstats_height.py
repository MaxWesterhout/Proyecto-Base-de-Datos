# Generated by Django 4.2.2 on 2023-06-30 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenis', '0006_alter_match_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playermatchstats',
            name='height',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
