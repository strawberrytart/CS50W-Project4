# Generated by Django 5.0.1 on 2024-01-27 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='network/profile_images/icon.jpg', null=True, upload_to='network/profile_images/'),
        ),
    ]