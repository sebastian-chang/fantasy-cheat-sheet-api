from django.db import models
from django.contrib.auth import get_user_model

# Create player model


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position=models.CharField(max_length=25)
    current_team=models.CharField(max_length=3)
    jersey_number = models.IntegerField(null=True, blank=True)
    height = models.CharField(max_length=6, blank=True)
    weight = models.IntegerField(blank=True)
    dob = models.CharField(max_length=10, blank=True)
    age = models.IntegerField(blank=True)
    city_team = models.CharField(max_length=100, blank=True)
    team_logo = models.CharField(max_length=200, blank=True)
    photo_url = models.CharField(max_length=200, blank=True)
    MSF_PID = models.IntegerField(null=True)
    has_stats = models.BooleanField(default=False)
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
