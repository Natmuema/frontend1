from django.contrib import admin
from .models import AssetCategory, Asset, AssetPrice

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'asset_type', 'category', 'current_price', 'currency', 'is_active']
    list_filter = ['asset_type', 'category', 'currency', 'is_active', 'created_at']
    search_fields = ['name', 'symbol', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['current_price', 'is_active']

@admin.register(AssetPrice)
class AssetPriceAdmin(admin.ModelAdmin):
    list_display = ['asset', 'price', 'volume', 'timestamp']
    list_filter = ['asset', 'timestamp']
    search_fields = ['asset__name', 'asset__symbol']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
