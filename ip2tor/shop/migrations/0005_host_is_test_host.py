# Generated by Django 4.1.5 on 2023-01-25 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_host_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='is_test_host',
            field=models.BooleanField(default=False, help_text='Test hosts cannot be extended indefinitely. The work during the first duration periods and then they die.', verbose_name='Is it a host for tests?'),
        ),
    ]
