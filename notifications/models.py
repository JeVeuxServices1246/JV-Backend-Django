# import uuid

# from django.db import models
# import datetime
# # Create your models here.
# from django.contrib.postgres.fields import ArrayField


# class Player(models.Model):
#     player_id = models.CharField(primary_key=True,max_length=100)
#     device_model = models.CharField(max_length=100, blank=True, null=True)
#     ip_address = models.CharField(max_length=100, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = u'"users_org_companies\".\"player"'

# class FcmUser(models.Model):
#     fcm_id = models.CharField(primary_key=True,max_length=100)
#     device_type = models.CharField(max_length=100, blank=True, null=True)
#     device_model = models.CharField(max_length=100, blank=True, null=True)
#     ip_address = models.CharField(max_length=100, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = u'"users_org_companies\".\"fcm_user"'

#     def __str__(self):
#         return self.fcm_id

# class UserNotificationSubscription(models.Model):
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE,db_column='user_id')
#     player_id = models.ForeignKey(Player, on_delete=models.CASCADE,db_column='player_id')
#     is_subscribed = models.BooleanField(default=False)
#     last_updated = models.DateTimeField(default=datetime.datetime.now, blank=True)

#     class Meta:
#         db_table = u'"users_org_companies\".\"user_notification_subscription"'

# class UserFcmSubscription(models.Model):
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE,db_column='user_id')
#     fcm_id = models.ForeignKey(FcmUser, on_delete=models.CASCADE,db_column='fcm_id')
#     is_subscribed = models.BooleanField(default=True)
#     is_logged_in = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = u'"users_org_companies\".\"user_fcm_subscription"'
#         unique_together = ('user_id', 'fcm_id',)

# class Notification(models.Model):
#     event_type = models.CharField(max_length=100, blank=True, null=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     description = models.CharField(max_length=1000, blank=True, null=True)
#     notification_data = models.CharField(max_length=1000, blank=True, null=True)
#     notification_time = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = u'"users_org_companies\".\"notification"'


# class UserNotification(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE,db_column='user_id')
#     notification = models.ForeignKey(Notification, on_delete=models.CASCADE,db_column='notification_id')
#     is_opened = models.BooleanField(default=False)

#     class Meta:
#         db_table = u'"users_org_companies\".\"user_notification"'
