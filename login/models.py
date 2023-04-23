
from django.db import models


class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'user_roles'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150, null=False, blank=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.IntegerField(default=1)
    phone_number = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, null=True, blank=False)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=64)
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, default=1)
    profile_pic = models.CharField(max_length=200, null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'users'


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.city

    class Meta:
        db_table = 'user_address'
        unique_together = ('street_address', 'house_number', 'city', 'state', 'zip_code')


class ServiceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'service_categories'


class ServiceSubcategory(models.Model):
    id = models.AutoField(primary_key=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='categories')
    parent_service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, null=True, related_name='parent_categories')
    
    class Meta:
        db_table = 'service_subcategories'


class Provider(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dl_front_image = models.CharField(max_length=200)
    dl_back_image = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    service_range = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'providers'


class ProviderServiceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'provider_categories'
        unique_together = ('provider', 'service_category')


class ProjectModule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'project_modules'


class UserPermission(models.Model):
    id = models.AutoField(primary_key=True)
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)
    project_module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_permissions'
        constraints = [
            models.UniqueConstraint(fields=['user_role', 'project_module'], name='unique_permission')
        ]
