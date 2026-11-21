
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

path('employees/', views.employee_list, name='employee_list'),
path('employees/add/', views.employee_add, name='employee_add'),
path('employees/edit/<int:employee_id>/', views.employee_edit, name='employee_edit'),
path('employees/toggle/<int:employee_id>/', views.employee_toggle_status, name='employee_toggle'),


path('leads/', views.lead_list, name='lead_list'),
path('leads/add/', views.lead_add, name='lead_add'),
path('leads/edit/<int:lead_id>/', views.lead_edit, name='lead_edit'),
path('leads/delete/<int:lead_id>/', views.lead_delete, name='lead_delete'),
path('leads/assign/<int:lead_id>/', views.lead_assign, name='lead_assign'),

path('call-centre/', views.call_centre, name='call_centre'),
path('calls/record/<int:lead_id>/', views.record_call, name='record_call'),
path('call-performance/', views.call_performance, name='call_performance'),

path('followups/', views.followup_list, name='followup_list'),
path('followups/add/<int:lead_id>/', views.followup_add, name='followup_add'),
path('followups/complete/<int:followup_id>/', views.followup_complete, name='followup_complete'),

path(
    'leads/bulk-upload/',
    views.bulk_lead_upload,
    name='bulk_lead_upload'
),

path(
    'leads/download-sample/',
    views.download_sample_csv,
    name='download_sample_csv'
),
path('banks/', views.bank_list, name='bank_list'),
path('banks/add/', views.bank_add, name='bank_add'),
path('banks/edit/<int:bank_id>/', views.bank_edit, name='bank_edit'),

path('loan-schemes/', views.scheme_list, name='scheme_list'),
path('loan-schemes/add/', views.scheme_add, name='scheme_add'),
path('loan-schemes/edit/<int:scheme_id>/', views.scheme_edit, name='scheme_edit'),
path(
    'applications/',
    views.application_list,
    name='application_list'
),

path(
    'applications/add/',
    views.application_add,
    name='application_add'
),
path(
    'applications/<int:application_id>/documents/',
    views.document_list,
    name='document_list'
),

path(
    'applications/<int:application_id>/documents/upload/',
    views.document_upload,
    name='document_upload'
),
path(
    'document-verification/',
    views.admin_document_verification,
    name='admin_document_verification'
),
path(
    'document-verification/<int:document_id>/',
    views.verify_document,
    name='verify_document'
),
path(
    'applications/<int:application_id>/update-status/',
    views.update_application_status,
    name='update_application_status'
),
path(
    'reports/',
    views.reports_analytics,
    name='reports_analytics'
),
path(
    'mobile-admin/',
    views.mobile_admin_dashboard,
    name='mobile_admin_dashboard'
),
]
