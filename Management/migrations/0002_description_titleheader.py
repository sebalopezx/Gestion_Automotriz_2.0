# Generated by Django 4.2.4 on 2023-11-19 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('description_small', models.CharField(max_length=255)),
                ('image_description', models.ImageField(upload_to='index/')),
            ],
        ),
        migrations.CreateModel(
            name='TitleHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_header', models.CharField(max_length=50)),
            ],
        ),
    ]
