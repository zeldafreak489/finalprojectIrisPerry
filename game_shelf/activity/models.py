from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ("play", "Started Playing"),
        ("complete", "Completed Game"),
        ("review", "Left a Review"),
        ("add", "Added to Library"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_title = models.CharField(max_length=255)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.activity_type} {self.game_title}"
