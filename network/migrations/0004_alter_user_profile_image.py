# Generated by Django 5.0.1 on 2024-01-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_comments_options_user_following_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='media/network/profile_images/icon.jpg', null=True, upload_to='network/profile_images/'),
        ),
    ]
