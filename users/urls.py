from users import views
from django.urls import path


urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('user/', views.AuthUserAPIView.as_view(), name='user'),
    path('register_child/', views.ChildRegistrationAPIView.as_view(), name='child')
]