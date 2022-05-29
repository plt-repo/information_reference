from django.db import models
from django.core.validators import FileExtensionValidator


class CreatedUpdatedTimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class Category(CreatedUpdatedTimeMixin):
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родительcкая категория')
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Document(CreatedUpdatedTimeMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    code = models.CharField(max_length=255, verbose_name='Обозначение документа')
    name = models.CharField(max_length=255, verbose_name='Наименование документа')
    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx'])],
        help_text='Файл документа (doc, docx)'
    )

    def __str__(self):
        return f'{self.code}-{self.name}'

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
