from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user, authenticate, login, logout
from django.middleware.csrf import get_token

from ..models.sheet import Sheet
from ..serializers import SheetSerializer, UserSerializer


class Sheets(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SheetSerializer

    def get(self, request):
        """Index request"""
        sheets = Sheet.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = SheetSerializer(sheets, many=True).data
        return Response({'sheets': data})

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['sheet']['owner'] = request.user.id
        # Serialize/create cheat shee
        sheet = SheetSerializer(data=request.data['sheet'])
        # If the sheet data is valid according to our serializer...
        if sheet.is_valid():
            # Save the created sheet & send a response
            sheet.save()
            return Response({'sheet': sheet.data}, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(sheet.errors, status=status.HTTP_400_BAD_REQUEST)


class SheetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """Show request"""
        sheet = get_object_or_404(Sheet, pk=pk)
        if not request.user.id == sheet.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this sheet')

        # Run the data through the serializer so it's formatted
        data = SheetSerializer(sheet).data
        return Response({'sheet': data})

    def delete(self, request, pk):
        """Delete request"""
        # Locate sheet to delete
        sheet = get_object_or_404(Sheet, pk=pk)
        # Check the sheet's owner agains the user making this request
        if not request.user.id == sheet.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this sheet')
        # Only delete if the user owns the sheet
        sheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Remove owner from request object
        # This "gets" the owner key on the data['sheet'] dictionary
        # and returns False if it doesn't find it. So, if it's found we
        # remove it.
        if request.data['sheet'].get('owner', False):
            del request.data['sheet']['owner']

        # Locate Sheet
        # get_object_or_404 returns a object representation of our Sheet
        sheet = get_object_or_404(Sheet, pk=pk)
        # Check if user is the same as the request.user.id
        if not request.user.id == sheet.owner.id:
            raise PermissionDenied('Unauthorized, you do not own this sheet')

        # Add owner to data object now that we know this user owns the resource
        request.data['sheet']['owner'] = request.user.id
        # Validate updates with serializer
        data = SheetSerializer(sheet, data=request.data['sheet'])
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response({'sheet': data.data}, status=status.HTTP_202_ACCEPTED)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
