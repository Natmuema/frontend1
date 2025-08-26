from django.urls import path
from . import views

urlpatterns = [
    # MeTTa Scripts
    path('scripts/', views.MettaScriptListCreateView.as_view(), name='script-list'),
    path('scripts/<int:pk>/', views.MettaScriptDetailView.as_view(), name='script-detail'),
    
    # MeTTa Executions
    path('executions/', views.MettaExecutionListCreateView.as_view(), name='execution-list'),
    path('executions/<int:pk>/', views.MettaExecutionDetailView.as_view(), name='execution-detail'),
    path('execute/', views.execute_metta_script, name='execute-script'),
    
    # MeTTa Data Mappings
    path('mappings/', views.MettaDataMappingListCreateView.as_view(), name='mapping-list'),
    path('mappings/<int:pk>/', views.MettaDataMappingDetailView.as_view(), name='mapping-detail'),
    
    # MeTTa Analysis
    path('analysis/', views.run_analysis, name='run-analysis'),
    path('analysis-results/', views.MettaAnalysisResultListView.as_view(), name='analysis-results'),
    
    # MeTTa Scheduled Tasks
    path('scheduled-tasks/', views.MettaScheduledTaskListCreateView.as_view(), name='scheduled-task-list'),
    path('scheduled-tasks/<int:pk>/', views.MettaScheduledTaskDetailView.as_view(), name='scheduled-task-detail'),
    
    # Data Export
    path('export/', views.export_data, name='export-data'),
    
    # Statistics
    path('statistics/', views.metta_statistics, name='metta-statistics'),
]