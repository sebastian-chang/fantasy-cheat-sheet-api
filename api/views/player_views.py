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

# Create your views here.
class Players(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayerSerializer

    def get(self, request):
        """Index request"""
        # Filter the mangos by owner, so you can only see your owned mangos
        # players = Player.objects.filter(owner=request.user.id)
        players = Player.objects.all()
        # Run the data through the serializer
        data = PlayerSerializer(players, many=True).data
        return Response({'players': data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        # request.data['player']['owner'] = request.user.id
        # Serialize/create mango
        player = PlayerSerializer(data=request.data['player'])
        # If the mango data is valid according to our serializer...
        if player.is_valid():
            # Save the created mango & send a response
            print(f"this is from the backend {request.data['player']}")
            player.save()
            return Response({'player': player.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(player.errors, status=status.HTTP_400_BAD_REQUEST)


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """Show request"""
        # Locate the mango to show
        player = get_object_or_404(Player, pk=pk)
        # Only want to show owned mangos?
        # if not request.user.id == player.owner.id:
        # raise PermissionDenied('Unauthorized, you do not own this mango')

        # Run the data through the serializer so it's formatted
        data = PlayerSerializer(player).data
        return Response({'player': data})

    def delete(self, request, pk):
        """Delete request"""
        # Locate mango to delete
        player = get_object_or_404(Mango, pk=pk)
        # Check the mango's owner agains the user making this request
        # if not request.user.id == player.owner.id:
        # raise PermissionDenied('Unauthorized, you do not own this mango')
        # Only delete if the user owns the  mango
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['mango'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        # if request.data['player'].get('owner', False):
        # del request.data['player']['owner']

        # Locate Mango
        # get_object_or_404 returns a object representation of our Mango
        player = get_object_or_404(Player, pk=pk)
        # Check if user is the same as the request.user.id
        # if not request.user.id == player.owner.id:
        # raise PermissionDenied('Unauthorized, you do not own this mango')

        # Add owner to data object now that we know this user owns the resource
        request.data['player']['owner'] = request.user.id
        # Validate updates with serializer
        data = PlayerSerializer(player, data=request.data['player'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
