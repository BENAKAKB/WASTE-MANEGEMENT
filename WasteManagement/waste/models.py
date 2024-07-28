

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  
        related_query_name='user'
    )

    

class WasteIssue(models.Model):
    ISSUE_TYPES = [
        ('General', 'General'),
        ('Electronic', 'Electronic'),
        ('Hazardous', 'Hazardous'),
    ]
    
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    reported_date = models.DateTimeField(default=timezone.now)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues', null=True)

    def __str__(self):
        return f"{self.issue_type} - {self.location}"

class PickupRequest(models.Model):
    item_description = models.TextField()
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    requested_date = models.DateTimeField(default=timezone.now)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pickups', null=True)

    def __str__(self):
        return f"{self.item_description} - {self.location}"
class UserImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded by {self.user.email}"