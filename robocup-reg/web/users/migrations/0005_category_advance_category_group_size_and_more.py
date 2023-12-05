# Generated by Django 4.2.8 on 2023-12-05 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_category_event_alter_person_diet'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='advance',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='category',
            name='group_size',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='category',
            name='list_of_results',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='ranking_params',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='soccer',
            field=models.BooleanField(default=False),
        ),
    ]
