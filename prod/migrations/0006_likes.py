# Generated by Django 4.2.7 on 2023-11-18 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0005_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_post', models.CharField(max_length=500)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
