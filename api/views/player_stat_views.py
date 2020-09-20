from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
# from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.qb_stat import QBStat
from ..serializers import QBStatsSerializer

from ..mysportsfeed.api import player_input


class QBStats(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QBStatsSerializer

    def get(self, request, pk):
        """Index request"""
        # Filter the players by owner, so you can only see your owned players
        print(f'looking for stats from player {pk}')
        player_stats = QBStat.objects.filter(pid=pk)
        # player_stats = Player.objects.all()
        # player_stats = get_object_or_404(QBStat, pid=pk)
        # Run the data through the serializer
        data = QBStatsSerializer(player_stats, many=True).data
        return Response({'player_stats': data})
