# Generated by Django 3.0.8 on 2021-02-02 01:17

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200716_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='attachment')),
            ],
        ),
        migrations.RemoveField(
            model_name='chat',
            name='msg_file',
        ),
        migrations.AddField(
            model_name='contact',
            name='profile_photo',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to='profilepic'),
        ),
        migrations.AddField(
            model_name='message',
            name='attachment',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(), upload_to=''),
        ),
        migrations.AddField(
            model_name='message',
            name='attachmentName',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='chat.Contact')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_notifications', to='chat.Message')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='notifications',
            field=models.ManyToManyField(blank=True, to='chat.Notification'),
        ),
    ]
