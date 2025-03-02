from django.urls import path
from .views import ProfileView, signup, loginMethod, get_users, delete_user, enable_user, change_role, logoutUser, api_get_users

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path("login", views.login, name="login"),
    path("signup/", signup, name="signup"),
    path("login/", loginMethod, name="login"),
    path("logout/", logoutUser, name="logout"),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path("users/", get_users, name="users"),
    path("api/users/", api_get_users, name="api_users"),
    path("enable_user/", enable_user, name="enable_user"),
    path("users/delete_user/", delete_user, name="delete_user"),
    path("users/change_role/", change_role, name="change_role"),
    # path("forgot_password", views.forgot_password, name="forgot_password"),
    # path("reset_password", views.reset_password, name="reset_password"),
]
