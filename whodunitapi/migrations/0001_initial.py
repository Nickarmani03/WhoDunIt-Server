# Generated by Django 3.2.7 on 2021-09-20 15:22

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
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('description', models.CharField(max_length=1000)),
                ('number_of_players', models.IntegerField()),
                ('director', models.CharField(max_length=50)),
                ('rating', models.CharField(max_length=6)),
                ('movie_image_url', models.CharField(max_length=255)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.genre')),
            ],
        ),
        migrations.CreateModel(
            name='MovieNight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('title', models.CharField(max_length=1000)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Suspect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('is_guilty', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=50)),
                ('profile_image_url', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NightPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_night', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.movienight')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.player')),
            ],
        ),
        migrations.AddField(
            model_name='movienight',
            name='attendees',
            field=models.ManyToManyField(related_name='attending', through='whodunitapi.NightPlayer', to='whodunitapi.Player'),
        ),
        migrations.AddField(
            model_name='movienight',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.player'),
        ),
        migrations.AddField(
            model_name='movienight',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.movie'),
        ),
        migrations.AddField(
            model_name='movie',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.player'),
        ),
        migrations.AddField(
            model_name='movie',
            name='suspect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whodunitapi.suspect'),
        ),
    ]
