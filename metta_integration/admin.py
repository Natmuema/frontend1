from django.contrib import admin
from .models import (MettaScript, MettaExecution, MettaDataMapping, 
                    MettaAnalysisResult, MettaScheduledTask)

@admin.register(MettaScript)
class MettaScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'script_type', 'user', 'is_active', 'created_at']
    list_filter = ['script_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']

@admin.register(MettaExecution)
class MettaExecutionAdmin(admin.ModelAdmin):
    list_display = ['script', 'user', 'status', 'started_at', 'completed_at']
    list_filter = ['status', 'started_at', 'completed_at']
    search_fields = ['script__name', 'user__username', 'error_message']
    readonly_fields = ['started_at', 'completed_at', 'execution_time']

@admin.register(MettaDataMapping)
class MettaDataMappingAdmin(admin.ModelAdmin):
    list_display = ['name', 'mapping_type', 'source_model', 'target_format', 'user', 'is_active']
    list_filter = ['mapping_type', 'is_active', 'created_at']
    search_fields = ['name', 'source_model', 'target_format', 'user__username']
    readonly_fields = ['created_at']
    list_editable = ['is_active']

@admin.register(MettaAnalysisResult)
class MettaAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['analysis_type', 'asset', 'portfolio', 'confidence_score', 'created_at']
    list_filter = ['analysis_type', 'created_at']
    search_fields = ['analysis_type', 'asset__name', 'portfolio__name']
    readonly_fields = ['created_at']

@admin.register(MettaScheduledTask)
class MettaScheduledTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'script', 'user', 'frequency', 'is_active', 'last_run', 'next_run']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['name', 'script__name', 'user__username']
    readonly_fields = ['last_run', 'next_run', 'created_at']
    list_editable = ['is_active']
