from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/message/', views.submit_message, name='submit_message'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/messages/<int:message_id>/status/', views.update_message_status, name='update_message_status'),
    path('dashboard/messages/<int:message_id>/notes/', views.update_admin_notes, name='update_admin_notes'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
