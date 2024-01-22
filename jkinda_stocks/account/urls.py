from django.urls import path
from .views import ProfileView, signup, loginMethod

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path("login", views.login, name="login"),
    path("signup/", signup, name="signup"),
    path("login/", loginMethod, name="login"),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    # path("forgot_password", views.forgot_password, name="forgot_password"),
    # path("reset_password", views.reset_password, name="reset_password"),
]
