from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
import json
import subprocess
import tempfile
import os
from .models import (MettaScript, MettaExecution, MettaDataMapping, 
                    MettaAnalysisResult, MettaScheduledTask)
from .serializers import (MettaScriptSerializer, MettaExecutionSerializer,
                         MettaDataMappingSerializer, MettaAnalysisResultSerializer,
                         MettaScheduledTaskSerializer, MettaScriptExecutionSerializer,
                         MettaAnalysisRequestSerializer, MettaDataExportSerializer)

class MettaScriptListCreateView(generics.ListCreateAPIView):
    serializer_class = MettaScriptSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['script_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    
    def get_queryset(self):
        return MettaScript.objects.filter(user=self.request.user)

class MettaScriptDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MettaScriptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MettaScript.objects.filter(user=self.request.user)

class MettaExecutionListCreateView(generics.ListCreateAPIView):
    serializer_class = MettaExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['script', 'status']
    ordering_fields = ['started_at', 'completed_at']
    
    def get_queryset(self):
        return MettaExecution.objects.filter(user=self.request.user)

class MettaExecutionDetailView(generics.RetrieveAPIView):
    serializer_class = MettaExecutionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MettaExecution.objects.filter(user=self.request.user)

class MettaDataMappingListCreateView(generics.ListCreateAPIView):
    serializer_class = MettaDataMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['mapping_type', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        return MettaDataMapping.objects.filter(user=self.request.user)

class MettaDataMappingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MettaDataMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MettaDataMapping.objects.filter(user=self.request.user)

class MettaAnalysisResultListView(generics.ListAPIView):
    serializer_class = MettaAnalysisResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['analysis_type', 'asset', 'portfolio']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        return MettaAnalysisResult.objects.filter(execution__user=self.request.user)

class MettaScheduledTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = MettaScheduledTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['frequency', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    
    def get_queryset(self):
        return MettaScheduledTask.objects.filter(user=self.request.user)

class MettaScheduledTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MettaScheduledTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return MettaScheduledTask.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def execute_metta_script(request):
    """Execute a MeTTa script"""
    serializer = MettaScriptExecutionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    script_id = serializer.validated_data['script_id']
    input_data = serializer.validated_data['input_data']
    execute_async = serializer.validated_data['execute_async']
    
    try:
        script = MettaScript.objects.get(id=script_id, user=request.user)
    except MettaScript.DoesNotExist:
        return Response({
            'error': 'Script not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Create execution record
    execution = MettaExecution.objects.create(
        script=script,
        user=request.user,
        status='pending',
        input_data=input_data
    )
    
    if execute_async:
        # For async execution, you would typically use Celery or similar
        # For now, we'll execute synchronously
        pass
    
    # Execute the MeTTa script
    try:
        execution.status = 'running'
        execution.save()
        
        # This is a placeholder for actual MeTTa execution
        # In a real implementation, you would:
        # 1. Save the script to a temporary file
        # 2. Execute MeTTa interpreter
        # 3. Capture output and errors
        # 4. Update execution record
        
        # Simulate execution
        import time
        time.sleep(2)  # Simulate processing time
        
        # Mock output data
        output_data = {
            'result': 'Script executed successfully',
            'data': input_data,
            'timestamp': timezone.now().isoformat()
        }
        
        execution.status = 'completed'
        execution.output_data = output_data
        execution.completed_at = timezone.now()
        execution.execution_time = execution.completed_at - execution.started_at
        execution.save()
        
        return Response({
            'execution_id': execution.id,
            'status': execution.status,
            'output': output_data
        })
        
    except Exception as e:
        execution.status = 'failed'
        execution.error_message = str(e)
        execution.completed_at = timezone.now()
        execution.save()
        
        return Response({
            'error': f'Script execution failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def run_analysis(request):
    """Run a MeTTa analysis"""
    serializer = MettaAnalysisRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    analysis_type = serializer.validated_data['analysis_type']
    asset_id = serializer.validated_data.get('asset_id')
    portfolio_id = serializer.validated_data.get('portfolio_id')
    parameters = serializer.validated_data.get('parameters', {})
    
    # Create a mock analysis result
    # In a real implementation, this would execute MeTTa analysis scripts
    
    result_data = {
        'analysis_type': analysis_type,
        'parameters': parameters,
        'timestamp': timezone.now().isoformat(),
        'results': {
            'confidence': 0.85,
            'recommendations': [
                'Consider diversifying your portfolio',
                'Monitor market trends closely',
                'Review risk tolerance'
            ]
        }
    }
    
    # Create analysis result record
    analysis_result = MettaAnalysisResult.objects.create(
        execution=None,  # Would be linked to actual execution
        analysis_type=analysis_type,
        asset_id=asset_id,
        portfolio_id=portfolio_id,
        result_data=result_data,
        confidence_score=0.85,
        recommendations=result_data['results']['recommendations']
    )
    
    return Response({
        'analysis_id': analysis_result.id,
        'analysis_type': analysis_type,
        'results': result_data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def export_data(request):
    """Export data in MeTTa-compatible format"""
    serializer = MettaDataExportSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data_type = serializer.validated_data['data_type']
    export_format = serializer.validated_data['format']
    filters = serializer.validated_data.get('filters', {})
    
    # This would export data in the specified format
    # For now, return a mock response
    
    export_data = {
        'data_type': data_type,
        'format': export_format,
        'filters': filters,
        'exported_at': timezone.now().isoformat(),
        'data': {
            'sample': 'This would contain actual exported data'
        }
    }
    
    return Response(export_data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def metta_statistics(request):
    """Get MeTTa integration statistics"""
    user = request.user
    
    total_scripts = MettaScript.objects.filter(user=user).count()
    active_scripts = MettaScript.objects.filter(user=user, is_active=True).count()
    total_executions = MettaExecution.objects.filter(user=user).count()
    successful_executions = MettaExecution.objects.filter(
        user=user, status='completed'
    ).count()
    total_analysis_results = MettaAnalysisResult.objects.filter(
        execution__user=user
    ).count()
    
    # Recent activity
    recent_executions = MettaExecution.objects.filter(
        user=user,
        started_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    return Response({
        'total_scripts': total_scripts,
        'active_scripts': active_scripts,
        'total_executions': total_executions,
        'successful_executions': successful_executions,
        'success_rate': (successful_executions / total_executions * 100) if total_executions > 0 else 0,
        'total_analysis_results': total_analysis_results,
        'recent_executions': recent_executions
    })
