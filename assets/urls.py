from django.urls import path
from . import views

urlpatterns = [
    # Asset Categories
    path('categories/', views.AssetCategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.AssetCategoryDetailView.as_view(), name='category-detail'),
    
    # Assets
    path('', views.AssetListCreateView.as_view(), name='asset-list'),
    path('<int:pk>/', views.AssetDetailView.as_view(), name='asset-detail'),
    path('search/', views.asset_search, name='asset-search'),
    path('statistics/', views.asset_statistics, name='asset-statistics'),
    
    # Asset Prices
    path('prices/', views.AssetPriceCreateView.as_view(), name='price-create'),
    path('<int:asset_id>/prices/', views.AssetPriceListView.as_view(), name='asset-prices'),
]