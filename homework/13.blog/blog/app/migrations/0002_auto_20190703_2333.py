# Generated by Django 2.2.2 on 2019-07-03 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='avatars/default.png', upload_to='avatars/'),
        ),
    ]
