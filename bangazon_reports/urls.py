from django.urls import path
from bangazon_reports.views.favorites.favorites import FavoriteListReport

from bangazon_reports.views.orders.allorders import OrderListReport
from .views import ProductListReport

urlpatterns = [
    path('products', ProductListReport.as_view()),
    path('orders', OrderListReport.as_view()),
    path('stores', FavoriteListReport.as_view()),
]