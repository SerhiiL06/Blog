# Generated by Django 4.0 on 2023-09-04 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_options_post_last_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='publiched',
            new_name='published',
        ),
    ]
