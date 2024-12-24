from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('product-details/<int:id>/', views.product_details, name='product-details'),
    path('main/<str:name>/', views.category, name='category'),
    path('categories/', views.category_summary, name='category_summary'),
    path('category-product/<str:product_brand>/', views.product_by_brand, name='product_by_brand'),
]
