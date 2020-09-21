from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token

from ..models.qb_stat import QBStat
from ..serializers import QBStatsSerializer

from ..mysportsfeed.api import player_input, player_stat_input


class QBStatDetails(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QBStatsSerializer

    def get(self, request, pk):
        """Index request"""
        # Filter the player stats by 3rd party player id
        player_stats = QBStat.objects.filter(pid=pk)
        data = QBStatsSerializer(player_stats, many=True).data
        return Response({'player_stats': data})

class QBStats(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QBStatsSerializer

    def post(self, request):
        """Create request"""
        stored = False
        check = 0
        # Add user to request data object
        # Serialize/create player
        # Sends user input data to 3rd party API
        player_stats = player_stat_input(request.data['player']['pid'], request.data['player']['year'])
        weeks = len(player_stats)
        for player_stat in player_stats:
            stat = QBStatsSerializer(data=player_stat)
            if stat.is_valid():
                stat.save()
                check += 1
        # Check to see if each week was successfully saved
        if (check == weeks):
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(player.errors, status=status.HTTP_400_BAD_REQUEST)
