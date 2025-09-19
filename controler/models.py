from django.db import models
from main.models import User

class WithdrawRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=7)
    reason = models.CharField(max_length=255, blank=True, null=True)
    bank = models.CharField(max_length=6 , blank=True , null=True)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
    
class T(models.Model):
    role = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    wnum = models.CharField(max_length=20)

    def __str__(self):
        return f"Role : {self.role} Name : {self.name}"