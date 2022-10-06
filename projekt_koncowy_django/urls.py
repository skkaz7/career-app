"""projekt_koncowy_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from career_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('app/', views.Base.as_view(), name='base'),
    path('accounts/', include('accounts.urls')),

    path('add/task/', views.AddTaskView.as_view(), name='add_task'),
    path('task/list/', views.TaskListView.as_view(), name='task_list'),
    path('task/<str:slug>/', views.TaskDetailView.as_view(), name='task_details'),
    path('task/update/<str:slug>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<str:slug>/', views.TaskDeleteView.as_view(), name='task_delete'),

    path('add/project/', views.AddProjectView.as_view(), name='add_project'),
    path('project/list/', views.ProjectListView.as_view(), name='project_list'),

    path('add/status/', views.AddStatusView.as_view(), name='add_status'),
    path('add/website/', views.AddWebsiteView.as_view(), name='add_website'),
    path('website/list/', views.WebsiteListView.as_view(), name='website_list'),
    path('add/company/', views.AddCompanyView.as_view(), name='add_company'),
    path('company/list/', views.CompanyListView.as_view(), name='company_list'),
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company_details'),
    path('add/job-offer/', views.AddJobOfferView.as_view(), name='add_job_offer'),
    path('job-offer/list/', views.JobOfferListView.as_view(), name='job_offer_list'),
    path('job-offer/update/<int:pk>/', views.JobOfferUpdateView.as_view(), name='job_offer_update'),
]
