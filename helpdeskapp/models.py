from django.db import models
from django.contrib.auth.models import User
from .models import ITuser


# Model of ITuser
class ITuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ituser')
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'ITuser'


# Models of category with issues
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# Ticket model
class Ticket(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(ITuser, on_delete=models.CASCADE, related_name='ticket_assigned_to', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_created_by')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

