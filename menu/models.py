from django.db import models
from django.utils import timezone
from django.urls import reverse


class Menu(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, default=None)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=100, default=None)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, default=None)
    menu = models.ForeignKey(Menu, blank=True, null=True, related_name='items', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='children')
    is_active = models.BooleanField(default=True)
    created = models.DateField(blank=True, null=True, default=timezone.now)
    updated = models.DateField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self, request):
        return request.build_absolute_uri(f'?selected={self.slug}')
