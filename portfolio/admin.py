from django.contrib import admin
from .models import Wallet, Portfolio, PortfolioHolding, Transaction, InvestmentAlert

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'currency', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__username', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']

@admin.register(PortfolioHolding)
class PortfolioHoldingAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'asset', 'quantity', 'average_purchase_price', 'total_value', 'profit_loss']
    list_filter = ['portfolio', 'asset', 'created_at']
    search_fields = ['portfolio__name', 'asset__name', 'asset__symbol']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'asset', 'quantity', 'total_amount', 'transaction_date']
    list_filter = ['transaction_type', 'transaction_date', 'portfolio']
    search_fields = ['user__username', 'asset__name', 'asset__symbol', 'notes']
    readonly_fields = ['transaction_date']
    ordering = ['-transaction_date']

@admin.register(InvestmentAlert)
class InvestmentAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'asset', 'alert_type', 'threshold_value', 'is_active', 'triggered_at']
    list_filter = ['alert_type', 'is_active', 'created_at', 'triggered_at']
    search_fields = ['user__username', 'asset__name', 'asset__symbol']
    readonly_fields = ['created_at', 'triggered_at']
    list_editable = ['is_active']
