from django.urls import path

from . import views2
from . import apiViews
from .views import dashboard

urlpatterns = [
    path("save_data", views2.save_data, name="save_data"),
    path("save_data2", views2.save_data2, name="save_data2"),
    path("save_data3", views2.save_data3, name="save_data3"),
    path("save_data4", views2.save_data4, name="save_data4"),
    path("show_data", views2.show_data, name="show_data"),
    path("compare_view", views2.compare_view, name="compare_view"),
    path("company/", views2.company, name="company"),
    path("company-list/", views2.company_list, name="company_list"),
    path("get_companies/<slug:search>", views2.get_companies, name="get_companies"),
    path("get_financials/<slug:symbol>", views2.get_financials, name="get_financials"),
    path("get_short_financials/<slug:symbol>", views2.get_short_financials, name="get_short_financials"),
    path("create_dashboard/", dashboard.create_dashboard, name="create_dashboard"),
    path("company_dropdown", views2.company_dropdown, name="company_dropdown"),
    path("update_company", views2.update_company, name="update_company"),
    path("", views2.index, name="home"),
    path("get_dashboards", dashboard.get_dashboards, name="get_dashboards"),
    path("create_chart", dashboard.create_chart, name="create_chart"),
    path("get_chart_data", dashboard.get_chart_data, name="get_chart_data"),
    path("delete_chart", dashboard.delete_chart, name="delete_chart"),
    path("chart_preview/<int:dashboard_id>/", dashboard.chart_preview, name="chart_preview"),
    path("api/get_dashboards/", apiViews.get_dashboards, name="get_dashboards"),
    path("api/add_chart_to_dashboard/", apiViews.add_chart_to_dashboard, name="add_chart_to_dashboard"),
    path("api/get_operators/", apiViews.get_operators, name="get_operators"),
]
