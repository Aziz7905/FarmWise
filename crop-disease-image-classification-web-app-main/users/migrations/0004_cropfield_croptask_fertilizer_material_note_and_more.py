# Generated by Django 5.0.6 on 2025-05-07 17:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_farmerpost_likes_alter_farmerpost_date_posted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CropField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('area', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stage', models.CharField(max_length=100)),
                ('next_action', models.CharField(max_length=200)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.farmerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='CropTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.farmerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Fertilizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fertilizers', to='users.farmerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('unit', models.CharField(default='units', max_length=20)),
                ('date', models.DateField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='users.farmerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.farmerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Pesticide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pesticides', to='users.farmerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TreeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tree_name', models.CharField(max_length=100)),
                ('count', models.PositiveIntegerField()),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trees', to='users.farmerprofile')),
            ],
        ),
    ]
