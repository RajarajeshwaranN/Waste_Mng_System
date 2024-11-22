# Generated by Django 5.1.3 on 2024-11-22 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_alter_admintask_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admintask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Assigned', 'Assigned'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
