# Generated by Django 4.2.7 on 2023-11-23 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prod', '0012_alter_post_user_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user_img',
        ),
    ]
