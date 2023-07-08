# Generated by Django 4.2.2 on 2023-06-30 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenis', '0004_alter_tournament_id_alter_ranking_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='level',
            field=models.CharField(default='M', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tournament',
            name='surface',
            field=models.CharField(choices=[('Hard', 'Hard'), ('Clay', 'Clay'), ('Grass', 'Grass'), ('Carpet', 'Carpet'), ('Unknown', 'Unknown')], default='Hard', max_length=10),
            preserve_default=False,
        ),
    ]