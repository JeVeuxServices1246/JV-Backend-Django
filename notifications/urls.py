from django.urls import path

# from pushNotifications.views import *
from .views import *

urlpatterns = [
    path('is_fcm_id_active/', is_fcm_id_active),
    path('test_notification/', test_notification),
    # path('get_user_data/', get_user_data),
    # path('update_subscription/', update_subscription),
    # path('toggle_subscription/', toggle_subscription),
    # path('get_new_notification_count/', get_new_notification_count),
    # path('get_notifications/', get_notifications),
    # path('open_notification/', open_notification),
    # path('test_notification/', test_notification),
    # path('check_app_update/', check_app_update),
    # path('transaction_sync_status/', transaction_sync_status),
    # path('customizable_bulk_notification/', customizable_bulk_notification),
    # path('on_logout/', on_logout),
    # path('delete_old_fcm_ids/', delete_old_fcm_ids),
]