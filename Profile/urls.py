from . import views
from django.urls import path

urlpatterns = [
    path('<int:user_id>/', views.profile, name="view"),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
]