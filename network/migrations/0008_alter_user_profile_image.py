# Generated by Django 5.0.1 on 2024-01-27 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='network/profile_images/'),
        ),
    ]
