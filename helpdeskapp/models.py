from django.db import models
from django.contrib.auth.models import User

# Model of ITuser
class ITuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ituser')
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'ITuser'

# Ticket model
class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    STATUS_CHOICES2 = (
        ('low', 'low'),
        ('mid', 'mid'),
        ('hight', 'hight'),
    )
    STATUS_CHOICES3 = (
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Network', 'Network'),
        ('Other', 'Other')
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    priority = models.CharField(max_length=100, choices=STATUS_CHOICES2, default='low')
    request_type = models.CharField(max_length=100, choices=STATUS_CHOICES3, default='Software')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(ITuser, on_delete=models.CASCADE, related_name='ticket_assigned_to', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_created_by')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title