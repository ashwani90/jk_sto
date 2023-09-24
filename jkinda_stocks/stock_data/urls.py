from django.urls import path

from . import views2
from .views import dashboard

urlpatterns = [
    path("save_data", views2.save_data, name="save_data"),
    path("save_data2", views2.save_data2, name="save_data2"),
    path("save_data3", views2.save_data3, name="save_data3"),
    path("save_data4", views2.save_data4, name="save_data4"),
    path("show_data", views2.show_data, name="show_data"),
    path("compare_view", views2.compare_view, name="compare_view"),
    path("company", views2.company, name="company"),
    path("create_dashboard", dashboard.create_dashboard, name="create_dashboard"),
    path("company_dropdown", views2.company_dropdown, name="company_dropdown"),
    path("update_company", views2.update_company, name="update_company"),
    path("", views2.index, name="home"),
    
]
