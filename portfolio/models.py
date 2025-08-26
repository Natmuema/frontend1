from django.db import models
from django.contrib.auth.models import User
from assets.models import Asset
from decimal import Decimal

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wallet - {self.currency} {self.balance}"
    
    def add_funds(self, amount):
        self.balance += amount
        self.save()
    
    def deduct_funds(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.name} Portfolio"
    
    @property
    def total_value(self):
        return sum(holding.total_value for holding in self.holdings.all())

class PortfolioHolding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    average_purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} ({self.quantity})"
    
    @property
    def total_value(self):
        return self.quantity * self.asset.current_price
    
    @property
    def total_cost(self):
        return self.quantity * self.average_purchase_price
    
    @property
    def profit_loss(self):
        return self.total_value - self.total_cost
    
    @property
    def profit_loss_percentage(self):
        if self.total_cost > 0:
            return (self.profit_loss / self.total_cost) * 100
        return 0

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    price_per_unit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.total_amount}"
    
    class Meta:
        ordering = ['-transaction_date']

class InvestmentAlert(models.Model):
    ALERT_TYPES = [
        ('price_above', 'Price Above'),
        ('price_below', 'Price Below'),
        ('percentage_change', 'Percentage Change'),
        ('volume_alert', 'Volume Alert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    threshold_value = models.DecimalField(max_digits=15, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.asset.name} {self.alert_type} Alert"
