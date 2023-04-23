from django.db import models 

from login.models import ServiceCategory, ServiceSubcategory, Provider, User

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    cost = models.FloatField(default=0)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT)
    image = models.CharField(max_length=200, default="services/back.png")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'services'


class ServiceCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    show_in_cart = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_cart'
        unique_together = ('user', 'service')


class ServiceBooking(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_booking'
        unique_together = ('user', 'service')


class AcceptServiceBooking(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accept_service_booking'


# class ServicePayment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service_id = models.CharField(max_length=100)
#     payment_id = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=10)
#     payment_status = models.CharField(max_length=20, default='Incomplete')

#     class Meta:
#         db_table = 'service_payment'

