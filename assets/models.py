from django.db import models
from django.contrib.auth.models import User

class AssetCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Asset Categories"

class Asset(models.Model):
    ASSET_TYPES = [
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('crypto', 'Cryptocurrency'),
        ('real_estate', 'Real Estate'),
        ('commodity', 'Commodity'),
        ('forex', 'Foreign Exchange'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20, blank=True, null=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE, related_name='assets')
    description = models.TextField(blank=True, null=True)
    current_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    metadata = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.symbol})" if self.symbol else self.name
    
    class Meta:
        unique_together = ['name', 'symbol']

class AssetPrice(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.asset.name} - ${self.price} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
