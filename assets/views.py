from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import AssetCategory, Asset, AssetPrice
from .serializers import (AssetCategorySerializer, AssetSerializer, AssetPriceSerializer,
                         AssetPriceCreateSerializer, AssetSearchSerializer)
from django.db import models

# Create your views here.

class AssetCategoryListCreateView(generics.ListCreateAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class AssetCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['asset_type', 'category', 'currency', 'is_active']
    search_fields = ['name', 'symbol', 'description']
    ordering_fields = ['name', 'current_price', 'created_at', 'updated_at']
    
    def get_queryset(self):
        return Asset.objects.filter(is_active=True)

class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class AssetPriceListView(generics.ListCreateAPIView):
    serializer_class = AssetPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['asset']
    ordering_fields = ['timestamp', 'price']
    
    def get_queryset(self):
        asset_id = self.kwargs.get('asset_id')
        if asset_id:
            return AssetPrice.objects.filter(asset_id=asset_id)
        return AssetPrice.objects.all()

class AssetPriceCreateView(generics.CreateAPIView):
    serializer_class = AssetPriceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def asset_search(request):
    serializer = AssetSearchSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    
    queryset = Asset.objects.filter(is_active=True)
    
    # Apply filters
    if serializer.validated_data.get('query'):
        query = serializer.validated_data['query']
        queryset = queryset.filter(
            models.Q(name__icontains=query) |
            models.Q(symbol__icontains=query) |
            models.Q(description__icontains=query)
        )
    
    if serializer.validated_data.get('asset_type'):
        queryset = queryset.filter(asset_type=serializer.validated_data['asset_type'])
    
    if serializer.validated_data.get('category_id'):
        queryset = queryset.filter(category_id=serializer.validated_data['category_id'])
    
    if serializer.validated_data.get('min_price'):
        queryset = queryset.filter(current_price__gte=serializer.validated_data['min_price'])
    
    if serializer.validated_data.get('max_price'):
        queryset = queryset.filter(current_price__lte=serializer.validated_data['max_price'])
    
    # Serialize results
    asset_serializer = AssetSerializer(queryset, many=True)
    return Response(asset_serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def asset_statistics(request):
    total_assets = Asset.objects.filter(is_active=True).count()
    assets_by_type = Asset.objects.filter(is_active=True).values('asset_type').annotate(
        count=models.Count('id')
    )
    total_categories = AssetCategory.objects.count()
    
    return Response({
        'total_assets': total_assets,
        'assets_by_type': assets_by_type,
        'total_categories': total_categories
    })
