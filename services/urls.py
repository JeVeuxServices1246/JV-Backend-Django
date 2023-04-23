from django.urls import path

from .views import *

urlpatterns = [
    path('service_categories/', service_categories),
    path('service_subcategories/', service_subcategories),
    path('add_service_category/', add_service_category),
    path('update_service_category/', update_service_category),

    path('services/', services),
    path('add_service/', add_service),
    path('update_service/', update_service),
    path('delete_service/', delete_service),

    path('add_to_cart/', add_to_cart),
    path('service_cart/', service_cart),
    path('save_service_for_later/', save_service_for_later),
    path('delete_service_from_cart/', delete_service_from_cart),
    
    path('service_bookings/', service_bookings),
    path('book_service/', book_service),
]