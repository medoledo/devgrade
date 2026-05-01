from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('projects/<slug:slug>/message/', views.submit_message, name='submit_message'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    # Auth
    path('admin-login/', views.admin_login, name='admin_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/messages/<int:message_id>/status/', views.update_message_status, name='update_message_status'),
    path('dashboard/messages/<int:message_id>/delete/', views.dashboard_message_delete, name='dashboard_message_delete'),
    # Category management
    path('dashboard/categories/', views.dashboard_categories, name='dashboard_categories'),
    path('dashboard/categories/add/', views.dashboard_category_add, name='dashboard_category_add'),
    path('dashboard/categories/<int:category_id>/edit/', views.dashboard_category_edit, name='dashboard_category_edit'),
    path('dashboard/categories/<int:category_id>/delete/', views.dashboard_category_delete, name='dashboard_category_delete'),
    # Project management
    path('dashboard/projects/', views.dashboard_projects, name='dashboard_projects'),
    path('dashboard/projects/add/', views.dashboard_project_add, name='dashboard_project_add'),
    path('dashboard/projects/<int:project_id>/edit/', views.dashboard_project_edit, name='dashboard_project_edit'),
    path('dashboard/projects/<int:project_id>/delete/', views.dashboard_project_delete, name='dashboard_project_delete'),
    path('dashboard/projects/<int:project_id>/images/<int:image_id>/delete/', views.dashboard_image_delete, name='dashboard_image_delete'),
    path('dashboard/projects/<int:project_id>/features/<int:feature_id>/delete/', views.dashboard_feature_delete, name='dashboard_feature_delete'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
