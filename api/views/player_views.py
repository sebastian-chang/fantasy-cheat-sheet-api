from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.player import Player
from ..serializers import PlayerSerializer, UserSerializer

from ..mysportsfeed.api import player_input


class Players(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayerSerializer

    def get(self, request):
        """Index request"""
        # Filter the players by owner, so you can only see your owned players
        players = Player.objects.filter(owner=request.user.id)
        # players = Player.objects.all()
        # Run the data through the serializer
        data = PlayerSerializer(players, many=True).data
        return Response({'players': data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['player']['owner'] = request.user.id
        # Serialize/create player
        # player = PlayerSerializer(data=request.data['player'])
        temp_player = player_input(request.data['player'])
        # print(f"this is from the OG  player before the save {temp_player}")
        player = PlayerSerializer(data=temp_player)
        # print(f"this is the fetched data {player}")
        # If the player data is valid according to our serializer...
        if player.is_valid():
            # Save the created player & send a response
            player.save()
            return Response({'player': player.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(player.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """Show request"""
        # Locate the player to show
        player = get_object_or_404(Player, pk=pk)
        # Only want to show owned player?
        if not request.user.id == player.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this player')

        # Run the data through the serializer so it's formatted
        data = PlayerSerializer(player).data
        return Response({'player': data})

    def delete(self, request, pk):
        """Delete request"""
        # Locate maplayerngo to delete
        player = get_object_or_404(Player, pk=pk)
        # Check the player's owner agains the user making this request
        if not request.user.id == player.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this player')
        # Only delete if the user owns the  player
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['player'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['player'].get('owner', False):
            del request.data['player']['owner']

        # Locate Player
        # get_object_or_404 returns a object representation of our Player
        player = get_object_or_404(Player, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == player.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this player')

        # Add owner to data object now that we know this user owns the resource
        request.data['player']['owner'] = request.user.id
        # Validate updates with serializer
        temp_player = player_input(request.data['player'])
        # data = PlayerSerializer(player, data=request.data['player'])
        data = PlayerSerializer(player, data=temp_player)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response({'player': data.data}, status=status.HTTP_202_ACCEPTED)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
