from rest_framework import serializers
from .models import AssetCategory, Asset, AssetPrice

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = ['id', 'name', 'description', 'created_at']

class AssetPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetPrice
        fields = ['id', 'price', 'volume', 'timestamp']

class AssetSerializer(serializers.ModelSerializer):
    category = AssetCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    price_history = AssetPriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Asset
        fields = ['id', 'name', 'symbol', 'asset_type', 'category', 'category_id',
                 'description', 'current_price', 'currency', 'metadata', 'created_by',
                 'created_at', 'updated_at', 'is_active', 'price_history']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'price_history']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class AssetPriceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetPrice
        fields = ['asset', 'price', 'volume']
    
    def create(self, validated_data):
        # Update the asset's current price when a new price is added
        asset_price = super().create(validated_data)
        asset = asset_price.asset
        asset.current_price = asset_price.price
        asset.save()
        return asset_price

class AssetSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)
    asset_type = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    min_price = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)