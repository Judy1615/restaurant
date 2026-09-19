from django.urls import path
from . import views

app_name = 'menu'


urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('search/', views.search_menu, name='search_menu'),
    path('add/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_update, name='item_update'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
]