from django.db import models
from django.contrib.auth.models import User

class SavedGame(models.Model):
    STATUS_CHOICES = [
        ("played", "Played"),
        ("playing", "Currently Playing"),
        ("want", "Want to Play"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rawg_id = models.IntegerField()
    title = models.CharField(max_length=200)
    cover_image = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="want")

    def __str__(self):
        return f"{self.title} ({self.user.username})"
