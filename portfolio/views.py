from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Q
from .models import Wallet, Portfolio, PortfolioHolding, Transaction, InvestmentAlert
from .serializers import (WalletSerializer, PortfolioSerializer, PortfolioHoldingSerializer,
                         TransactionSerializer, TransactionCreateSerializer,
                         InvestmentAlertSerializer, PortfolioSummarySerializer)

class WalletView(generics.RetrieveUpdateAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        wallet, created = Wallet.objects.get_or_create(user=self.request.user)
        return wallet

class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user, is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class PortfolioHoldingListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioHoldingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['portfolio']
    ordering_fields = ['created_at', 'updated_at']
    
    def get_queryset(self):
        return PortfolioHolding.objects.filter(portfolio__user=self.request.user)

class PortfolioHoldingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioHoldingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PortfolioHolding.objects.filter(portfolio__user=self.request.user)

class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['transaction_type', 'asset', 'portfolio', 'wallet']
    ordering_fields = ['transaction_date', 'total_amount']
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class InvestmentAlertListCreateView(generics.ListCreateAPIView):
    serializer_class = InvestmentAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['asset', 'alert_type', 'is_active']
    ordering_fields = ['created_at', 'triggered_at']
    
    def get_queryset(self):
        return InvestmentAlert.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InvestmentAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvestmentAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return InvestmentAlert.objects.filter(user=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def portfolio_summary(request):
    user = request.user
    
    # Get portfolio statistics
    portfolios = Portfolio.objects.filter(user=user, is_active=True)
    total_portfolios = portfolios.count()
    
    total_value = sum(portfolio.total_value for portfolio in portfolios)
    
    # Calculate total profit/loss
    holdings = PortfolioHolding.objects.filter(portfolio__user=user)
    total_profit_loss = sum(holding.profit_loss for holding in holdings)
    
    # Calculate average profit/loss percentage
    total_cost = sum(holding.total_cost for holding in holdings)
    if total_cost > 0:
        total_profit_loss_percentage = (total_profit_loss / total_cost) * 100
    else:
        total_profit_loss_percentage = 0
    
    # Count active alerts
    active_alerts = InvestmentAlert.objects.filter(user=user, is_active=True).count()
    
    summary_data = {
        'total_portfolios': total_portfolios,
        'total_value': total_value,
        'total_profit_loss': total_profit_loss,
        'total_profit_loss_percentage': total_profit_loss_percentage,
        'active_alerts': active_alerts
    }
    
    serializer = PortfolioSummarySerializer(summary_data)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def buy_asset(request):
    """Execute a buy transaction"""
    serializer = TransactionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    wallet = Wallet.objects.get(user=user)
    
    # Check if user has enough funds
    if wallet.balance < serializer.validated_data['total_amount']:
        return Response({
            'error': 'Insufficient funds in wallet'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create transaction
    transaction = serializer.save(
        user=user,
        transaction_type='buy',
        wallet=wallet
    )
    
    # Deduct funds from wallet
    wallet.deduct_funds(transaction.total_amount)
    
    # Update or create portfolio holding
    portfolio = transaction.portfolio
    asset = transaction.asset
    quantity = transaction.quantity
    
    holding, created = PortfolioHolding.objects.get_or_create(
        portfolio=portfolio,
        asset=asset,
        defaults={
            'quantity': quantity,
            'average_purchase_price': transaction.price_per_unit
        }
    )
    
    if not created:
        # Update existing holding
        total_quantity = holding.quantity + quantity
        total_cost = (holding.quantity * holding.average_purchase_price) + \
                    (quantity * transaction.price_per_unit)
        holding.average_purchase_price = total_cost / total_quantity
        holding.quantity = total_quantity
        holding.save()
    
    return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sell_asset(request):
    """Execute a sell transaction"""
    serializer = TransactionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    wallet = Wallet.objects.get(user=user)
    portfolio = serializer.validated_data['portfolio']
    asset = serializer.validated_data['asset']
    quantity = serializer.validated_data['quantity']
    
    # Check if user has enough assets to sell
    try:
        holding = PortfolioHolding.objects.get(portfolio=portfolio, asset=asset)
        if holding.quantity < quantity:
            return Response({
                'error': 'Insufficient assets to sell'
            }, status=status.HTTP_400_BAD_REQUEST)
    except PortfolioHolding.DoesNotExist:
        return Response({
            'error': 'No holding found for this asset'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create transaction
    transaction = serializer.save(
        user=user,
        transaction_type='sell',
        wallet=wallet
    )
    
    # Add funds to wallet
    wallet.add_funds(transaction.total_amount)
    
    # Update portfolio holding
    holding.quantity -= quantity
    if holding.quantity <= 0:
        holding.delete()
    else:
        holding.save()
    
    return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
