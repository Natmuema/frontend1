from django.urls import path
from . import views

urlpatterns = [
    # Wallet
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    
    # Portfolios
    path('portfolios/', views.PortfolioListCreateView.as_view(), name='portfolio-list'),
    path('portfolios/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('summary/', views.portfolio_summary, name='portfolio-summary'),
    
    # Portfolio Holdings
    path('holdings/', views.PortfolioHoldingListCreateView.as_view(), name='holding-list'),
    path('holdings/<int:pk>/', views.PortfolioHoldingDetailView.as_view(), name='holding-detail'),
    
    # Transactions
    path('transactions/', views.TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),
    path('buy/', views.buy_asset, name='buy-asset'),
    path('sell/', views.sell_asset, name='sell-asset'),
    
    # Investment Alerts
    path('alerts/', views.InvestmentAlertListCreateView.as_view(), name='alert-list'),
    path('alerts/<int:pk>/', views.InvestmentAlertDetailView.as_view(), name='alert-detail'),
]