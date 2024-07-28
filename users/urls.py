from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views

app_name = 'users'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
