# Generated by Django 4.2.7 on 2023-11-23 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0015_alter_post_user_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_post_images'),
        ),
    ]
