# Generated by Django 5.0.3 on 2024-04-17 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_caregiverlevel_wait_time'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='person',
            unique_together={('first_name', 'last_name')},
        ),
    ]