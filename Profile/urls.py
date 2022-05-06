from . import views
from django.urls import path

urlpatterns = [
    path('<int:user_id>/', views.profile, name="view"),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.login, name='login'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),

]