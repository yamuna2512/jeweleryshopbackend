from django.db import models
class User(models.Model):
    first_name = models.CharField(
        'Firstname', blank=False, null=False, max_length=50
    )
    last_name = models.CharField(
        'Lastname', blank=False, null=False, max_length=50
    )
    email = models.EmailField(
        'Email', blank=False, null=False, max_length=100, unique=True
    )
    phone = models.CharField(
        'Phone', max_length=15, blank=False, null=False
    )
    password = models.CharField(
        'Password', blank=False, null=False, max_length=255
    )
    created_at = models.DateTimeField(
        'Creation Date', auto_now_add=True
    )
    token = models.CharField(
        'Token', blank=True, null=True, max_length=500, db_index=True
    )
    token_expires = models.DateTimeField(
        'Token Expiration Date', blank=True, null=True
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}"