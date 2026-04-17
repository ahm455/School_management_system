from django.db import models
from services.common import CreateUpdateTime
from accounts.models import User
from services.constants import NotificationChoices


class Notification(CreateUpdateTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=50,choices=NotificationChoices)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return self.title