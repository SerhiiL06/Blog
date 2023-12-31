# Generated by Django 4.0 on 2023-09-05 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verification',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.UUIDField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('validity_period', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
