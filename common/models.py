from django.db import models
from login.models import ProjectModule, UserPermission
from datetime import datetime, timedelta


class Banner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    image = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True)
    expiry_time = models.DateTimeField(default=datetime.now() + timedelta(days=1))

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'banners'