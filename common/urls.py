from django.urls import path

from .views import *

urlpatterns = [
    path('home/', home),
    path('upload_image/', upload_image),
    path('add_project_module/', add_project_module),
    path('user_permissions/', user_permissions),
    path('add_user_permission/', add_user_permission),
    
    path('banners/', banners),
    path('add_banner/', add_banner),
    path('update_banner/', update_banner),
    path('delete_banner/', delete_banner),
]