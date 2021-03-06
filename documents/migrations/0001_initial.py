# Generated by Django 2.2.20 on 2022-05-28 17:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='documents.Category', verbose_name='Родительcкая категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('code', models.CharField(max_length=255, verbose_name='Обозначение документа')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование документа')),
                ('file', models.FileField(help_text='Файл документа (doc, docx)', upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['doc', 'docx'])])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.Category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
    ]
