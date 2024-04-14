from django.db import models
from django.urls import reverse


# Create your models here.

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    menu_name = models.CharField(max_length=100)
    level = models.IntegerField(verbose_name='Уровень глубины', null=True)
    url = models.SlugField(verbose_name='absolute_path', max_length=255, null=True)

    def get_absolute_url(self):
        return reverse('menu', kwargs={"menu_path": self.url})

    def get_path(self):
        """
        Метод для формирования URL для объекта меню в зависимости от его родителей.
        """
        url = ''
        if self.parent:
            # Если у объекта есть родитель, добавляем URL родителя
            url += f'{self.parent.get_path()}/'
        url += f'{self.name}'
        return url

    def __str__(self):
        return self.name




