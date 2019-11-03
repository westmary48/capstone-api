from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sizeyourdriveapi.models import Donator
from django.contrib.auth.models import User



class DonatorSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Donators

    Arguments:
        serializers
    """
    class Meta:
        model = Donator
        url = serializers.HyperlinkedIdentityField(
            view_name='donator',
            lookup_field = 'id'

        )
        fields = ('id', 'url', 'user', 'phone_number', 'address')
        depth = 1


class Donators(ViewSet):
    """Donators
    Methods: GET PUT(id) POST
"""

    def create(self, request):
        """Handle POST operations
        Methods:  POST
        Returns:
            Response -- JSON serialized Donator instance
        """
        new_donator = Donator()
        new_donator.phone_number = request.data["phone_number"]
        new_donator.address = request.data["address"]

        user = Donator.objects.get(user=request.auth.user)
        new_donator.user = user

        new_donator.save()
        serializer = DonatorSerializer(new_donator, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single donator
        Methods:  GET
        Returns:
            Response -- JSON serialized donator instance
        """
        try:
            donator = Donator.objects.get(pk=pk)
            serializer = DonatorSerializer(donator, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a donator
        Returns:
            Response -- Empty body with 204 status code
        """
        user = User.objects.get(pk=request.auth.user.id)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.save()

        donator = Donator.objects.get(user=user)
        donator.address = request.data["address"]
        donator.phone_number = request.data["phone_number"]
        donator.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to donators resource
       Methods:  GET
        Returns:
            Response -- JSON serialized list of park areas
        """
        donators = Donator.objects.all()
        people = list(donators)
        serializer = DonatorSerializer(
            donators, many=True, context={'request': request})

        return Response(serializer.data)