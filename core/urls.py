from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.reports),
    path('generate_reports_sports/', views.generate_report_sports),
    path('generate_reports_items/', views.generate_report_items),
    path('generate_reports_fines/', views.generate_report_fines),
]