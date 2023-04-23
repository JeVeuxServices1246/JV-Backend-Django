# import json
# import pprint
# import datetime
# import time
# from datetime import timedelta
# import requests
# from django.db.models import Q

# from pushNotifications.models import *

# from tally_push_notifications.settings import WEBAPP_URL, API_DOMAIN_URL, FCM_SERVER_KEY
# import logging

# logger = logging.getLogger('send_bulk_notification')


# class UpdateNotifierFcm(object):

#     def __init__(self, **notifier_data):
#         self.title = notifier_data.get("title")
#         self.description = notifier_data.get("description")
#         self.web_url = notifier_data.get("web_url", None)
#         self.event_type = notifier_data.get("event_type")
#         self.url_type = notifier_data.get("url_type", None)
#         self.device_type_list = notifier_data.get("device_type_list", None)

#     def send_notification(self, data):
#         fcm_ids = data["fcm_ids"]
#         notification_data = data["notification_data"]

#         # header = {"Content-Type": "application/json; charset=utf-8",
#         #           "Authorization": "Basic {}".format(ONESIGNAL_CLIENT_ID)}
#         headers = {
#             "Content-Type": "application/json; charset=utf-8",
#             "Authorization": "key=" + FCM_SERVER_KEY,
#         }

#         body = {
#             'notification': {
#                 'title': self.title,
#                 'body': self.description
#             },
#             'registration_ids': fcm_ids,
#             'priority': 'high',
#             'data': {
#                 'notification_data': notification_data,
#                 'web_url': self.web_url,
#                 'event_type' : self.event_type
#             },
#         }

#         if self.url_type == "webapp":
#             body["data"]["app_url"] = ""
#         else:
#             body["data"]["app_url"] = self.web_url if self.web_url else ""

#         response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))

#         response_data = {}
#         if response.status_code == 200:
#             response_data["data"] = json.loads(response.content)
#             response_data["status"] = True
#             response_data["message"] = "Notification sent"
#         else:
#             response_data["data"] = json.loads(response.content)
#             response_data["status"] = False
#             response_data["message"] = "Notification not sent"

#         # print(response_data)
#         return response_data

#     def send_update(self):
#         response_data = {"status": False, "data": None, "response": ""}
#         if self.device_type_list:
#             all_filtered_fcm_ids = FcmUser.objects.filter(device_model__in=self.device_type_list)
#             all_fcm_users = UserFcmSubscription.objects.distinct("fcm_id").filter(Q(is_logged_in=True), Q(is_subscribed=True), Q(fcm_id__in=all_filtered_fcm_ids))
#         else:
#             all_fcm_users = UserFcmSubscription.objects.distinct("fcm_id").filter(Q(is_logged_in=True), Q(is_subscribed=True))
#         # print(all_fcm_users)

#         start_limit = 0
#         end_limit = 20
#         user_limit = 20

#         notification_data = dict()
#         notification_data["event_type"] = self.event_type
#         notification_data["category"] = "new_feature"
#         notification_data["web_url"] = self.web_url

#         # notification_data_json = json.dumps(notification_data)
#         # event_type = notification_data["event_type"]

#         # notification_obj = Notification.objects.create(
#         #                             event_type=event_type,
#         #                             title=self.title,
#         #                             description=self.description,
#         #                             notification_data=notification_data_json)
#         # notification_data["notification_id"] = notification_obj.id

#         notified_users = 0
#         while True:
#             selected_users = all_fcm_users[start_limit:end_limit]
#             if len(selected_users) == 0:
#                 break

#             fcm_ids = []
#             for selected_user in selected_users:
#                 fcm_ids.append(str(selected_user.fcm_id))

#                 # curr_user = Users.objects.get(u_uuid=selected_user.user_id.u_uuid)
#                 #
#                 # try:
#                 #     UserNotification.objects.get(user=curr_user,
#                 #                                  notification=notification_obj)
#                 # except UserNotification.DoesNotExist:
#                 #     UserNotification.objects.create(
#                 #         user=curr_user,
#                 #         notification=notification_obj)
#             sending_data = {"fcm_ids": fcm_ids,
#                             "notification_data": notification_data}
#             response = self.send_notification(sending_data)
#             time.sleep(1)
#             if response.get("status", False):
#                 notified_users += len(fcm_ids)
#             logger.info(response)
#             start_limit += user_limit
#             end_limit += user_limit

#         response_data["data"] = {"notified_users": notified_users}
#         response_data["status"] = True
#         response_data["response"] = "Update Notification Sent"
#         # logger.info(response_data)
#         return response_data
