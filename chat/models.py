from django.db import models
from django.contrib.auth.models import User
from helpdeskapp.models import Ticket
# w trakcie tworzenia
class Notification(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)