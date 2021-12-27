# Generated by Django 3.2.9 on 2021-12-26 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fantaland_app', '0003_alter_mylocation_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.DecimalField(decimal_places=5, default=-76.61219, max_digits=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='lon',
            field=models.DecimalField(decimal_places=5, default=-76.61219, max_digits=15),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='attraction',
            unique_together={('name', 'location')},
        ),
        migrations.AlterUniqueTogether(
            name='restaurant',
            unique_together={('name', 'location')},
        ),
    ]