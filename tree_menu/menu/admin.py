from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'menu_name', 'level', 'get_absolute_url')
    list_filter = ('menu_name', 'parent', 'level')
    search_fields = ('name',)
    # Это улучшит интерфейс выбора родителя при создании или редактировании в случае большой вложенности
    raw_id_fields = ('parent',)


admin.site.register(MenuItem, MenuItemAdmin)
