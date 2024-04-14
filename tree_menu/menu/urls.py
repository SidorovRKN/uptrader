from django.urls import path
from . import views

urlpatterns = [
    path('<path:menu_path>/', views.menu_detail, name='menu'),
    path('', views.menu_detail, name='menu'),

]
