# Generated by Django 4.0 on 2023-09-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='last_update',
            field=models.DateTimeField(editable=False),
        ),
    ]
