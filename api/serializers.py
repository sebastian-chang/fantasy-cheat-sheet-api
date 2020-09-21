from django.contrib.auth import get_user_model
from rest_framework import serializers

# from .models.mango import Mango
from .models.sheet import Sheet
from .models.player import Player
from .models.qb_stat import QBStat
from .models.user import User


class PlayerSerializer(serializers.ModelSerializer):
    # This model serializer is for player information
    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'position',
                  'height', 'weight', 'dob', 'age', 'city_team', 'team_logo',
                  'jersey_number', 'current_team', 'photo_url', 'MSF_PID', 'has_stats', 'sheet', 'owner')


class SheetSerializer(serializers.ModelSerializer):
    # This model serializer is for user's cheat sheets
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Sheet
        fields = ('title', 'owner', 'players', 'id')

class QBStatsSerializer(serializers.ModelSerializer):
    # This model serializer is for player seasonal stats
    class Meta:
        model = QBStat
        fields = ('id', 'pid', 'week', 'season', 'opponent', 'homeoraway',
                  'passattempts', 'passattempts', 'passcompletions', 'passpct', 'passyards',
                  'passavg', 'passyardsperatt', 'passtd', 'passint', 'passlng', 'passsacks',
                  'passtdpct', 'passintpct',
                  'pass20plus', 'pass40plus', 'qbrating')


class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        # change back to 5 for password length
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserLoginSerializer(UserSerializer):
    # Require email, password for sign in
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(
        required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError(
                'Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                'Please make sure your passwords match.')
        # if all is well, return the data
        return data


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)
