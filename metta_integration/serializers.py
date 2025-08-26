from rest_framework import serializers
from .models import (MettaScript, MettaExecution, MettaDataMapping, 
                    MettaAnalysisResult, MettaScheduledTask)

class MettaScriptSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MettaScript
        fields = ['id', 'name', 'description', 'script_type', 'code', 'user',
                 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MettaExecutionSerializer(serializers.ModelSerializer):
    script = MettaScriptSerializer(read_only=True)
    script_id = serializers.IntegerField(write_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MettaExecution
        fields = ['id', 'script', 'script_id', 'user', 'status', 'input_data',
                 'output_data', 'error_message', 'execution_time', 'started_at', 'completed_at']
        read_only_fields = ['id', 'user', 'status', 'output_data', 'error_message',
                           'execution_time', 'started_at', 'completed_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MettaDataMappingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MettaDataMapping
        fields = ['id', 'name', 'mapping_type', 'source_model', 'target_format',
                 'mapping_rules', 'user', 'is_active', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MettaAnalysisResultSerializer(serializers.ModelSerializer):
    execution = MettaExecutionSerializer(read_only=True)
    asset_name = serializers.ReadOnlyField(source='asset.name')
    portfolio_name = serializers.ReadOnlyField(source='portfolio.name')
    
    class Meta:
        model = MettaAnalysisResult
        fields = ['id', 'execution', 'analysis_type', 'asset', 'asset_name',
                 'portfolio', 'portfolio_name', 'result_data', 'confidence_score',
                 'recommendations', 'created_at']
        read_only_fields = ['id', 'created_at']

class MettaScheduledTaskSerializer(serializers.ModelSerializer):
    script = MettaScriptSerializer(read_only=True)
    script_id = serializers.IntegerField(write_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MettaScheduledTask
        fields = ['id', 'name', 'script', 'script_id', 'user', 'frequency',
                 'cron_expression', 'is_active', 'last_run', 'next_run', 'created_at']
        read_only_fields = ['id', 'user', 'last_run', 'next_run', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class MettaScriptExecutionSerializer(serializers.Serializer):
    script_id = serializers.IntegerField()
    input_data = serializers.JSONField(default=dict)
    execute_async = serializers.BooleanField(default=False)

class MettaAnalysisRequestSerializer(serializers.Serializer):
    analysis_type = serializers.ChoiceField(choices=MettaAnalysisResult.ANALYSIS_TYPES)
    asset_id = serializers.IntegerField(required=False)
    portfolio_id = serializers.IntegerField(required=False)
    parameters = serializers.JSONField(default=dict)

class MettaDataExportSerializer(serializers.Serializer):
    data_type = serializers.ChoiceField(choices=[
        ('assets', 'Assets'),
        ('portfolio', 'Portfolio'),
        ('transactions', 'Transactions'),
        ('analysis_results', 'Analysis Results'),
    ])
    format = serializers.ChoiceField(choices=[
        ('json', 'JSON'),
        ('csv', 'CSV'),
        ('xml', 'XML'),
    ])
    filters = serializers.JSONField(default=dict)