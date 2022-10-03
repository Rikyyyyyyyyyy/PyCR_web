"""Tproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from Profile import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Profile.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('profile/', include(('Profile.urls', 'Profile'), namespace='account')),
    path('profile/<user_id>', views.profile, name='profile'),
    path('profile/<user_id>/edit/', views.edit_profile_view, name='edit'),
    path('featureselection/task', views.feature_task_list, name='feature_task_list'),
    path('featureselection/tasks/upload/', views.feature_upload_task, name='feature_upload_task'),
    path('delete/feature/<int:pk>/', views.delete_feature_task, name='delete_feature_task'),
    path('BuyMeCofee/', views.buyMeCoffee, name='buyMeCoffee'),
    path('BuyMeCofee/charge', views.stripe_charge, name='charge'),
    path('BuyMeCofee/success/<str:args>/', views.stripe_success, name='success'),
    path('about/', views.about, name='aboutPage'),
    path('about/cite', views.about_cite, name='about_citePage'),
    path('about/contributor', views.about_contributor, name='about_contributorPage'),
    path('about/support', views.about_support, name='about_supportPage'),
    path('about/project', views.about_project, name='about_projectPage'),
    path('about/license', views.about_license, name='about_licensePage'),
    path('about/privacy', views.about_privacy, name='about_privacyPage'),
    path('about/instruction', views.about_instruction, name='about_instructionPage'),
    path('others/', views.others, name='others'),
    path('others/1dreconstruct', views.others_1dreconstruct, name='others-1dreconstruct'),
    path('others/1dreconstruct/upload', views.others_1drecontruct_upload_task, name='1drecontruct_upload_task'),
    path('delete/idconstruct/<int:pk>/', views.delete_1dreconstruct_task, name='delete_1dconstruct_task'),
    path('featureselection/download/<int:pk>/', views.create_presigned_url, name='presign_url'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)