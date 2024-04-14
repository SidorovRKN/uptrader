from django.shortcuts import render


# Create your views here.
def menu_detail(request, menu_path=None):
    return render(request, 'menu/menu_detail.html')
