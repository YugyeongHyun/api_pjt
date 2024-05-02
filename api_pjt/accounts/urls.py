from django.urls import path
from .views import UserRegistrationView, MyTokenObtainPairView, UserProfileView

urlpatterns = [
    path('', UserRegistrationView.as_view(), name='register'),
    path('login', MyTokenObtainPairView.as_view(),
         name='login'),
    path('<str:username>',
         UserProfileView.as_view(), name='profile'),]
