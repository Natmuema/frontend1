from rest_framework import serializers
from .models import Wallet, Portfolio, PortfolioHolding, Transaction, InvestmentAlert
from assets.serializers import AssetSerializer

class WalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'currency', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class PortfolioHoldingSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.IntegerField(write_only=True)
    total_value = serializers.ReadOnlyField()
    total_cost = serializers.ReadOnlyField()
    profit_loss = serializers.ReadOnlyField()
    profit_loss_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = PortfolioHolding
        fields = ['id', 'portfolio', 'asset', 'asset_id', 'quantity', 'average_purchase_price',
                 'total_value', 'total_cost', 'profit_loss', 'profit_loss_percentage',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class PortfolioSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    holdings = PortfolioHoldingSerializer(many=True, read_only=True)
    total_value = serializers.ReadOnlyField()
    
    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'name', 'description', 'is_active', 'total_value',
                 'holdings', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'total_value', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.IntegerField(write_only=True, required=False)
    portfolio_name = serializers.ReadOnlyField(source='portfolio.name')
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'asset', 'asset_id', 'quantity',
                 'price_per_unit', 'total_amount', 'portfolio', 'portfolio_name',
                 'wallet', 'transaction_date', 'notes']
        read_only_fields = ['id', 'user', 'transaction_date']

class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'asset', 'quantity', 'price_per_unit',
                 'total_amount', 'portfolio', 'wallet', 'notes']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class InvestmentAlertSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = InvestmentAlert
        fields = ['id', 'user', 'asset', 'asset_id', 'alert_type', 'threshold_value',
                 'is_active', 'created_at', 'triggered_at']
        read_only_fields = ['id', 'user', 'created_at', 'triggered_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PortfolioSummarySerializer(serializers.Serializer):
    total_portfolios = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_profit_loss = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_profit_loss_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    active_alerts = serializers.IntegerField()