import json
# import pprint
# import datetime
# from datetime import timedelta
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import *
# from django.core.exceptions import ObjectDoesNotExist
from jvservices.settings import FCM_SERVER_KEY
# from pushNotifications.update_notifier_fcm import UpdateNotifierFcm
# import logging
# from babel.numbers import format_currency
# from user_agents import parse
# from django.shortcuts import redirect
# from django.db.models import Q


@api_view(['POST'])
def is_fcm_id_active(request):
    fcm_id = request.data.get('fcm_id')
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "key=" + FCM_SERVER_KEY,
    }
    response = requests.get("https://iid.googleapis.com/iid/info/"+fcm_id, headers=headers)
    if response.status_code == 200:
        is_active = True
    else:
        is_active = False
    return Response({'is_active': is_active})


@api_view(['POST'])
def test_notification(request):
    title = request.data.get('title', None)
    description = request.data.get('description', None)
    fcm_ids = request.data.get('fcm_ids', [])
    
    if title and description and fcm_ids:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "key=" + FCM_SERVER_KEY,
        }

        data = {
            'notification': {
                'title': title,
                'body': description
            },
            'registration_ids': fcm_ids,
            'priority': 'high',
            'data': {
                "notification_data": {}
            },
        }

        try:
            response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(data))
            response_data = {}
            if response.status_code == 200:
                response_data["data"] = json.loads(response.content)
                response_data["status"] = True
                response_data["message"] = "Notification sent"
            else:
                response_data["data"] = str(response.content)
                response_data["status"] = False
                response_data["message"] = "Notification not sent"
        except BaseException as e:
            response_data["message"] = f"Error: {e}"
    else:
        response_data["message"] = "title, description and fcm_ids are mandatory"
    return Response(response_data)


def send_notification(data):
    title = data["title"]
    description = data["description"]
    # notification_data = data["notification_data"]
    fcm_id = data["fcm_id"]

    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "to": fcm_id,
        "notification": {
            "title": "title",
            "body": "message"
        }
    }

    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(data))
    response_data = {}
    if response.status_code == 200:
        response_data["data"] = json.loads(response.content)
        response_data["status"] = True
        response_data["message"] = "Notification sent"
    else:
        response_data["data"] = str(response.content)
        response_data["status"] = False
        response_data["message"] = "Notification not sent"
    return response_data


def send_bulk_notification(data):
    title = data["title"]
    description = data["description"]
    # notification_data = data["notification_data"]
    fcm_ids = data["fcm_ids"]

    # web_page = data["web_page"]
    # event_type = notification_data["event_type"] if "event_type" in notification_data.keys() else None
    # if web_page:
    #     url = "{}/#/{}".format(WEBAPP_URL, web_page)
    # else:
    #     url = None

    # data = {
    #     'notification': {
    #         'title': title,
    #         'body': description
    #     },
    #     'registration_ids': fcm_ids,
    #     'priority': 'high',
    #     'data': {
    #         "web_url": url,
    #         "app_url": "",
    #         "notification_data": notification_data
    #     },
    # }
    
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "key=" + FCM_SERVER_KEY,
    }

    data = {
        'notification': {
            'title': title,
            'body': description
        },
        'registration_ids': fcm_ids,
        'priority': 'high',
        'data': {
            "notification_data": data
        },
    }

    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(data))
    response_data = {}
    if response.status_code == 200:
        response_data["data"] = json.loads(response.content)
        response_data["status"] = True
        response_data["message"] = "Notification sent"
    else:
        response_data["data"] = str(response.content)
        response_data["status"] = False
        response_data["message"] = "Notification not sent"
    return response_data


# @api_view(['GET'])
# def delete_old_fcm_ids(request):
#     response_data = {"status": True, "data": None}

#     try:
#         all_fcm_ids = FcmUser.objects.all()

#         valid_fcm_ids = []
#         expired_fcm_id_objects = []
#         delete_count = 0

#         for i in all_fcm_ids:
#             curr_fcm_id = str(i)
#             curr_fcm_id_status = is_fcm_id_active(curr_fcm_id)
#             if curr_fcm_id_status:
#                 valid_fcm_ids.append(curr_fcm_id)
#             else:
#                 expired_fcm_id_objects.append(i)
#                 delete_count += 1
#         try:
#             FcmUser.objects.filter(fcm_id__in=expired_fcm_id_objects).delete()
#             response_data["message"] = "Expired Fcm_ids deleted."
#         except:
#             response_data["message"] = "Expired Fcm_ids not deleted.."
#         response_data['valid_fcm_ids'] = valid_fcm_ids
#         response_data['delete_count'] = delete_count
#     except:
#         response_data["status"] = False
#         response_data["message"] = "Unable to access DataBase."
#     return Response(response_data)

# @api_view(['POST'])
# def get_user_data(request):
#     # {
#     #     "fcm_id" : "canx6hR_SkCce6yT3bbNX1:APA91bHfUxH_5i-tfKrSd0f5wLnwKr5KrBOK4Vsz3a_A-9yXrCENgK4hs1U1mnczWI7cJm65q_ZmJM_nhb38qTpfFYS1ibBeDYcqCTYkb9MuxOU_1TWQi3uHVRD6Kk8HuDed2r-_nhrC",
#     #     "user_id":"5878d061-b421-43da-b912-f3a3ff6b4e26",
#     #     "device_type" : "Android",
#     #     "device_model" : "RealMe GT Master Edition",
#     #     "ip_address" : "10.100.72.110",
#     # }

#     user_id = request.data.get('user_id')
#     fcm_id = request.data.get('fcm_id')
#     device_type = request.data.get('device_type')
#     device_model = request.data.get('device_model')
#     ip_address = request.data.get('ip_address')
#     old_fcm_id = request.data.get('old_fcm_id', None)

#     response_data = {"status": True, "data": None}

#     try:
#         user = Users.objects.get(u_uuid=user_id)
#         try:
#             fcm_user = FcmUser.objects.get(fcm_id=fcm_id)
#         except FcmUser.DoesNotExist:
#             fcm_user = FcmUser.objects.create(
#                 fcm_id=fcm_id,
#                 device_type=device_type,
#                 device_model=device_model,
#                 ip_address=ip_address,
#             )
#         response_data["data"] = {
#             "user_id": user_id,
#             "fcm_id": fcm_id,
#             "is_subscribed": True
#         }
#         user_fcm_ids = UserFcmSubscription.objects.filter(Q(fcm_id=fcm_id), Q(user_id=user_id))
#         if len(user_fcm_ids) > 0:
#             user_fcm_ids.update(is_logged_in=True)
#             response_data["data"]["is_subscribed"] = user_fcm_ids[0].is_subscribed
#             response_data["message"] = 'FCM User Found'
#         else:
#             UserFcmSubscription.objects.create(
#                 user_id=user,
#                 fcm_id=fcm_user
#             )
#             response_data["message"] = 'FCM User Saved'

#         if old_fcm_id:
#             FcmUser.objects.filter(fcm_id=old_fcm_id).delete()

#     except Users.DoesNotExist:
#         response_data["status"] = False
#         response_data["message"] = "User does not exist"
#     return Response(response_data)


# @api_view(['POST'])
# def on_logout(request):
#     user_id = request.data.get('user_id')
#     fcm_id = request.data.get('fcm_id')

#     response_data = {"status": True, "data": None}

#     status = UserFcmSubscription.objects.filter(fcm_id=fcm_id, user_id=user_id).update(is_logged_in=False)

#     if status > 0:
#         response_data["message"] = "User Logged Out Successfully"
#         response_data["data"] = request.data
#     else:
#         response_data["status"] = False
#         response_data["message"] = "User Not Found"

#     return Response(response_data)


# @api_view(['POST'])
# def toggle_subscription(request):
#     """This api is used to update subscription status in UserNotificationSubscription table in DB
#     {"user_id":"30c74ef0-951b-42d4-9237-08a1e4a34c33",
#     "fcm_id":"ab3659fa-14c6-4b0f-b71c-b5c0d41697c6",
#     "is_subscribed":true}"""

#     user_id = request.data.get('user_id')
#     fcm_id = request.data.get('fcm_id')
#     is_subscribed = request.data.get('is_subscribed')

#     response_data = {"status": True}

#     try:
#         user = Users.objects.get(u_uuid=user_id)
#         try:
#             fcm_user = FcmUser.objects.get(fcm_id=fcm_id)
#             try:
#                 notification_subscription = UserFcmSubscription.objects.get(user_id=user, fcm_id=fcm_user)

#                 notification_subscription.is_subscribed = is_subscribed
#                 notification_subscription.last_updated = datetime.datetime.now()
#                 notification_subscription.save()

#                 response_data["data"] = request.data

#             except UserFcmSubscription.DoesNotExist:
#                 response_data["data"] = None
#                 response_data["status"] = False
#                 response_data["message"] = "User not subscribed"

#         except FcmUser.DoesNotExist:
#             response_data["data"] = None
#             response_data["status"] = False
#             response_data["message"] = "FCM ID does not exist"

#     except Users.DoesNotExist:
#         response_data["data"] = None
#         response_data["status"] = False
#         response_data["message"] = "User does not exist"

#     print(response_data)
#     return Response(response_data)


# def save_notification(data):
#     notification_data = data["notification_data"]
#     notification_data_json = json.dumps(notification_data)
#     event_type = notification_data["event_type"]

#     notification = Notification.objects.create(
#         event_type=event_type,
#         title=data["title"],
#         description=data["description"],
#         notification_data=notification_data_json)

#     try:
#         UserNotification.objects.get(user=data["user_id"], notification=notification)
#     except UserNotification.DoesNotExist:
#         UserNotification.objects.create(
#             user=data["user_id"],
#             notification=notification)

#     data["user_id"] = data["user_id"].u_uuid
#     notification_data["notification_id"] = notification.id
#     data["data"] = notification_data
#     del data["notification_data"]
#     return data


# def send_notification(data):
#     title = data["title"]
#     description = data["description"]
#     notification_data = data["notification_data"]
#     user_ids = data["user_ids"]
#     web_page = data["web_page"]

#     event_type = notification_data["event_type"] if "event_type" in notification_data.keys() else None

#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Authorization": "key=" + FCM_SERVER_KEY,
#     }

#     if web_page:
#         url = "{}/#/{}".format(WEBAPP_URL, web_page)
#     else:
#         url = None

#     fcm_ids = []
#     fcm_users = UserFcmSubscription.objects.filter(Q(user_id__in=user_ids), Q(is_subscribed=True), Q(is_logged_in=True))
#     for fcm_user in fcm_users:
#         fcm_ids.append(str(fcm_user.fcm_id))
#     print(fcm_ids, '***********')

#     body = {
#         'notification': {
#             'title': title,
#             'body': description
#         },
#         'registration_ids': fcm_ids,
#         'priority': 'high',
#         'data': {
#             "web_url": url,
#             "app_url": "",
#             "notification_data": notification_data
#         },
#     }

#     response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
#     response_data = {}
#     if response.status_code == 200:
#         response_data["data"] = json.loads(response.content)
#         response_data["status"] = True
#         response_data["message"] = "Notification sent"
#     else:
#         response_data["data"] = str(response.content)
#         response_data["status"] = False
#         response_data["message"] = "Notification not sent"
#     return response_data


# @api_view(['POST'])
# def open_notification(request):
#     """
#     This endpoint marks/updates a new user notification as old/opened

#     POST:
#         {
#             "user_id":"f9d686b5-5adb-4fb0-8063-30570bcfd067",
#             "notification_id": 1
#         }"""
#     user_id = request.data.get('user_id')
#     notification_id = request.data.get('notification_id')
#     try:
#         user = Users.objects.get(u_uuid=user_id)
#         user_notification = UserNotification.objects.get(user=user,
#                                                          notification_id=notification_id)
#         user_notification.is_opened = True
#         user_notification.save()

#         response_data = {"status": True, "message": "Notification opened",
#                          "data": {"notification_id": notification_id}}

#     except ObjectDoesNotExist:
#         response_data = {"status": False, "message": "User Notification not found",
#                          "data": None}
#     print(response_data)
#     return Response(response_data)


# @api_view(['POST'])
# def get_new_notification_count(request):
#     """
#     This endpoint returns count of all new notifications for a user since last month

#     POST:
#         {
#             "user_id":"f9d686b5-5adb-4fb0-8063-30570bcfd067"
#         }"""
#     user_id = request.data.get('user_id')
#     try:
#         user = Users.objects.get(u_uuid=user_id)
#         last_month = datetime.datetime.now() - timedelta(days=30)
#         new_count = UserNotification.objects.filter(user=user, is_opened=False,
#                                                     notification__notification_time__gte=last_month).count()
#         if new_count > 0:
#             response_data = {"status": True, "message": "You have new notifications",
#                              "data": {"count": new_count}}
#         else:
#             response_data = {"status": False, "message": "No new notifications",
#                              "data": {"count": 0}}
#     except Users.DoesNotExist:
#         response_data = {"status": False, "message": "User not found",
#                          "data": None}
#     print(response_data)
#     return Response(response_data)


# @api_view(['POST'])
# def get_notifications(request):
#     """
#     POST:
#         {
#             "user_id":"54af8147-0658-4363-b2f0-4ba2bd9ecefa",
#             "offset":0,
#             "limit":10
#         }"""
#     user_id = request.data.get('user_id')
#     offset = request.data.get('offset', 0)
#     limit = request.data.get('limit', 10) + offset
#     try:
#         user = Users.objects.get(u_uuid=user_id)
#         user_notifications = UserNotification.objects.filter(user=user).select_related().order_by('-id')[offset:limit]
#         notifications = []
#         for user_notification in user_notifications:
#             # notification = Notification.objects.get(id=user_notification.notification.id)
#             notification = user_notification.notification
#             notifications.append({"notification_id": notification.id,
#                                   "data": json.loads(notification.notification_data),
#                                   "description": notification.description,
#                                   "notification_time": notification.notification_time.strftime("%d %b %Y at %H:%M %p"),
#                                   "is_opened": user_notification.is_opened})

#         if len(notifications) > 0:
#             response_data = {"status": True, "message": "Notifications retrieved",
#                              "offset": offset, "data": notifications}
#         else:
#             response_data = {"status": False, "message": "Notifications not found",
#                              "data": None}

#     except ObjectDoesNotExist:
#         response_data = {"status": False, "message": "User does not exist",
#                          "data": None}

#     except BaseException as e:
#         response_data = {"data": None, "status": False, "message": str(e)}
#     print(response_data)
#     return Response(response_data)


# @api_view(['GET'])
# def test_notification(request):
#     """
#     This endpoint sends notification to user

#     GET: ?userid=f9d686b5-5adb-4fb0-8063-30570bcfd067
#     ?userid=1127cde1-70c3-45e8-a553-0006a12ee91e
#     """
#     # title = "Finsights"
#     # description = "new notification"
#     # # user_id = request.GET.get('userid', None)
#     # # user_ids = [user_id]
#     # # user_ids = ["1127cde1-70c3-45e8-a553-0006a12ee91e"]
#     # # player_ids = ["2a2ee388-74cb-425b-bfc0-25d7c8f2e044"]
#     # player_ids = ["2eb8102c-5d8c-11ec-9561-927662868002"]
#     # # print(user_ids)
#     # # ext_user_ids = ["7c3fb2fe-4107-45c6-b642-c7f8e08a8bac"] # don't use..
#     #
#     # header = {"Content-Type": "application/json; charset=utf-8",
#     #           "Authorization": "Basic {}".format(ONESIGNAL_CLIENT_ID)}

#     sending_data = {
#         'title': 'Hi',
#         'description': 'okay ?',
#         "user_ids": ["adac70b1-86a9-4986-81bb-ed8f5571d34d"],
#         'web_page': 'https://developers.google.com/instance-id/reference/server#python',
#         'notification_data': {}
#     }

#     # payload = {
#     #     # "include_external_user_ids": user_ids,
#     #     "include_player_ids":player_ids,
#     #     "app_id": ONESIGNAL_APP_ID,
#     #     "contents": {"en": description},
#     #     "headings": {"en": title},
#     #     "data": {},
#     #     # "web_url": "https://onesignal.com",
#     #     # "app_url": "http://app.finsights.biz/#/search" #replace app url
#     # }

#     # response = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
#     response = send_notification(sending_data)

#     print(response)
#     # response_data = json.loads(response) #.content
#     return Response(response)


# @api_view(['POST'])
# def customizable_bulk_notification(request):
#     """
#     This endpoint sends an update notification to all registered users with modifiable payload..
#     *title & description are mandatory..
#     POST:
#         {
#             "title" : "Beta Version of Quick Invoicing is now available",
#             "description" : "Please try the new Quick Invoice mode to raise GST compliant Invoices and let us know your feedback.",
#             "event_type" : "quick_invoice",
#             "web_url" : "#/quick-invoice",
#             "url_type" : "webapp"
#         }
#         {
#             "title" : "New update available",
#             "description" : "Update the app to get new notifications.",
#             "event_type" : "new_feature",
#             "web_url" : "tallypushnotificationsapi/api/check_app_update/",
#             "url_type" : "api"
#         }
#         {
#             "title" : "Get all Tally Registers on your Whatsapp",
#             "description" : "Click here to get your weekly and Monthly Sales, Purchase, Payments  and expense registers on Whatsapp.",
#             "event_type" : "pdf_report_alert",
#             "web_url" : "#/alerts-automations",
#             "url_type" : "webapp"
#         }
#     """
#     title = request.data.get('title')
#     description = request.data.get('description')
#     event_type = request.data.get('event_type', "new_feature")
#     web_url = request.data.get('web_url', None)
#     url_type = request.data.get('url_type', None)
#     device_type_list = request.data.get('device_type_list', None)

#     response_data = {"status": False, "data": None, "response": ""}

#     if title and description:

#         if web_url:
#             if url_type == "api":
#                 web_url = "{}/{}".format(API_DOMAIN_URL, web_url)
#             elif url_type == "webapp":
#                 web_url = "{}/{}".format(WEBAPP_URL, web_url)

#         notifier_data = {"title": title, "description": description, "web_url": web_url,
#                          "event_type": event_type, "url_type": url_type, "device_type_list": device_type_list}
#         update_notifier_obj = UpdateNotifierFcm(**notifier_data)
#         response_data = update_notifier_obj.send_update()

#         logger = logging.getLogger('customizable_bulk_notification')
#         logger.info(request.data)
#         logger.info(response_data)
#     else:
#         response_data["response"] = "Please provide title & description"
#     return Response(response_data)


# @api_view(['GET'])
# def check_app_update(request):
#     """
#         This endpoint redirects to Finsights app on play store or app store
#         based on user request
#     """
#     logger = logging.getLogger('check_app_update')
#     logger.info(request.META['HTTP_USER_AGENT'])
#     try:
#         user_agent = parse(request.META['HTTP_USER_AGENT'])
#         user_platform = user_agent.os.family
#     except Exception as e:
#         logger.error(str(e))
#         user_platform = "Android"
#     user_platform = user_platform.lower()
#     logger.info("User Platform: {}".format(user_platform))
#     if "ios" in user_platform or "mac" in user_platform:
#         return redirect("https://apps.apple.com/in/app/finsights-for-tally/id1571729090")
#     else:
#         return redirect("https://play.google.com/store/apps/details?id=com.finsights.finsights")
