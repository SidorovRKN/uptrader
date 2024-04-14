from django.urls import path
from . import views

urlpatterns = [
    path('menu/<path:menu_path>/', views.menu_detail, name='menu'),
    path('menu/', views.menu_detail, name='menu'),

]
