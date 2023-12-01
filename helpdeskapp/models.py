"""
    Represents a ticket in the helpdesk system.

    Attributes:
        title (str): The title of the ticket.
        description (str): The description of the ticket.
        status (str): The status of the ticket. Can be one of 'Pending', 'In Progress', or 'Completed'.
        priority (str): The priority of the ticket. Can be one of 'low', 'mid', or 'high'.
        request_type (str): The type of request for the ticket. Can be one of 'Software', 'Hardware', 'Network', or 'Other'.
        created_at (datetime): The date and time when the ticket was created.
        assigned_to (ITuser): The IT user assigned to the ticket.
        updated_at (datetime): The date and time when the ticket was last updated.
        created_by (User): The user who created the ticket.
    """
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
        ('high', 'high'),
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