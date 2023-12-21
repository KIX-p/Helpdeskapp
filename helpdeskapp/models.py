from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
    
# Ticket model
class Ticket(models.Model):
    """
    Represents a ticket in the helpdesk system.

    Attributes:
        title (str): The title of the ticket.
        description (str): The description of the ticket.
        status (str): The status of the ticket. Choices are 'Pending', 'In Progress', or 'Completed'.
        priority (str): The priority of the ticket. Choices are 'low', 'mid', or 'high'.
        request_type (str): The type of request for the ticket. Choices are 'Software', 'Hardware', 'Network', or 'Other'.
        created_at (datetime): The date and time when the ticket was created.
        assigned_to (User): The user assigned to the ticket.
        updated_at (datetime): The date and time when the ticket was last updated.
        created_by (User): The user who created the ticket.
        closed_at (datetime): The date and time when the ticket was closed.
        slug (str): The slugified version of the ticket title, used for generating a unique URL.
    """
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
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_assigned_to', null=True, blank=True, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_created_by')
    closed_at = models.DateTimeField(null=True, blank=True, default=None)
    
    objects = models.Manager() # default manager

    slug = models.SlugField(unique=True, default='default-slug')

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug if it doesn't exist.
        """
        if not self.id:
            self.slug = slugify(self.title)
            counter = 2
            while Ticket.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)



    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_change_status', 'Can change status'),#Ituser
            ('can_change_priority', 'Can change priority'),#Ituser
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('helpdeskapp:ticket_detail', args=[self.slug])
