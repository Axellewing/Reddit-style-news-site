# Generated by Django 4.2.7 on 2023-11-23 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0008_followercount'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to=''),
        ),
    ]
