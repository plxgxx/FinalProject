from django.urls import path

from . import views
app_name = 'CarHour'

urlpatterns = [
    path('', views.welcome_page, name='index'),
    path('takecar/', views.take_car, name='taking'),
    path('return/', views.return_car, name='returning'),
    path('add_car/', views.add_car, name='add_car'),
]