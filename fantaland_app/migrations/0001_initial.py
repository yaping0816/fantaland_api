# Generated by Django 3.2.9 on 2021-12-28 20:56

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
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=255)),
                ('lat', models.DecimalField(decimal_places=5, max_digits=15)),
                ('lon', models.DecimalField(decimal_places=5, max_digits=15)),
            ],
            options={
                'unique_together': {('lat', 'lon')},
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('categories', models.CharField(blank=True, max_length=255)),
                ('image_url', models.URLField(blank=True)),
                ('api_id', models.CharField(max_length=255, unique=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurants', to='fantaland_app.location')),
            ],
        ),
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('api_id', models.CharField(max_length=255, unique=True)),
                ('kinds', models.CharField(blank=True, max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attractions', to='fantaland_app.location')),
            ],
        ),
        migrations.CreateModel(
            name='MyLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attractions', models.ManyToManyField(blank=True, related_name='my_locations', to='fantaland_app.Attraction')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_locations', to='fantaland_app.location')),
                ('restaurants', models.ManyToManyField(blank=True, related_name='my_locations', to='fantaland_app.Restaurant')),
                ('traveller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_locations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('traveller', 'location')},
            },
        ),
    ]
