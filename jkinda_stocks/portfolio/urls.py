from django.urls import path
from .views import create_portfolio, get_portfolios, get_stocks, add_stock, delete_portfolio, get_chart_data

urlpatterns = [
    path("create/", create_portfolio, name="portfolio_create"),
    path("", get_portfolios, name="portfolio"),
    path("portfolio_stocks/", get_stocks, name="get_portfolio_stocks"),
    path("add_stock/", add_stock, name="add_stock"),
    path("delete_portfolio/<slug:id>", delete_portfolio, name="delete_portfolio"),
    path("get_chart_data/", get_chart_data, name="get_chart_data")
    # path("forgot_password", views.forgot_password, name="forgot_password"),
    # path("reset_password", views.reset_password, name="reset_password"),
]
