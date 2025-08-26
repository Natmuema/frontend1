from django.db import models
from django.contrib.auth.models import User
from assets.models import Asset
from portfolio.models import Portfolio

class MettaScript(models.Model):
    SCRIPT_TYPES = [
        ('analysis', 'Market Analysis'),
        ('prediction', 'Price Prediction'),
        ('optimization', 'Portfolio Optimization'),
        ('risk_assessment', 'Risk Assessment'),
        ('custom', 'Custom Script'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    script_type = models.CharField(max_length=20, choices=SCRIPT_TYPES)
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metta_scripts')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.script_type})"

class MettaExecution(models.Model):
    EXECUTION_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    script = models.ForeignKey(MettaScript, on_delete=models.CASCADE, related_name='executions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metta_executions')
    status = models.CharField(max_length=20, choices=EXECUTION_STATUS, default='pending')
    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, null=True)
    execution_time = models.DurationField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.script.name} - {self.status} at {self.started_at}"
    
    class Meta:
        ordering = ['-started_at']

class MettaDataMapping(models.Model):
    MAPPING_TYPES = [
        ('asset_data', 'Asset Data'),
        ('portfolio_data', 'Portfolio Data'),
        ('market_data', 'Market Data'),
        ('user_data', 'User Data'),
    ]
    
    name = models.CharField(max_length=200)
    mapping_type = models.CharField(max_length=20, choices=MAPPING_TYPES)
    source_model = models.CharField(max_length=100)
    target_format = models.CharField(max_length=100)
    mapping_rules = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metta_mappings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.mapping_type})"

class MettaAnalysisResult(models.Model):
    ANALYSIS_TYPES = [
        ('trend_analysis', 'Trend Analysis'),
        ('risk_assessment', 'Risk Assessment'),
        ('portfolio_optimization', 'Portfolio Optimization'),
        ('price_prediction', 'Price Prediction'),
        ('market_sentiment', 'Market Sentiment'),
    ]
    
    execution = models.ForeignKey(MettaExecution, on_delete=models.CASCADE, related_name='analysis_results')
    analysis_type = models.CharField(max_length=30, choices=ANALYSIS_TYPES)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, blank=True, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, blank=True, null=True)
    result_data = models.JSONField()
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    recommendations = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.analysis_type} - {self.asset.name if self.asset else 'Portfolio'}"

class MettaScheduledTask(models.Model):
    FREQUENCY_CHOICES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    
    name = models.CharField(max_length=200)
    script = models.ForeignKey(MettaScript, on_delete=models.CASCADE, related_name='scheduled_tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='metta_scheduled_tasks')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    cron_expression = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(blank=True, null=True)
    next_run = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.frequency}"
