from django.db import models
from django.contrib.auth import get_user_model

# Create player model


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position=models.CharField(max_length=25)
    current_team=models.CharField(max_length=100)
    photo_url=models.CharField(max_length=200, blank=True)
    MSF_PID=models.IntegerField(null=True)
    owner=models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    sheet=models.ForeignKey(
        'Sheet',
        related_name='players',
        null=True,
        on_delete=models.CASCADE
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.position} for the {self.current_team}'

    def as_dict(self):
        """Returns dictionary version of Player models"""
        return {
            'id': self.id,
            'first': self.first_name,
            'last': self.last_name,
            'position': self.position,
            'team': self.current_team,
            'photo': self.photo_url
        }
