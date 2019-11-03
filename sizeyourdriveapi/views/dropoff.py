from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sizeyourdriveapi.models import Dropoff, Donator


class DropoffSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Dropoff
    Arguments:
        serializers
    """
    class Meta:
        model = Dropoff
        url = serializers.HyperlinkedIdentityField(
            view_name='dropoff',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'organization', 'dropoff_date', 'create_date')


class Dropoffs(ViewSet):


    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized dropoff instance
        """
        new_dropoff = Dropoff()
        new_dropoff.name = request.data["name"]
        new_dropoff.organization = request.data["organization"]
        new_dropoff.dropoff_date = request.data["dropoff_date"]
        new_dropoff.create_date = request.data["create_date"]
        donator = Donator.objects.get(user=request.auth.user)
        new_dropoff.donator = donator
        new_dropoff.save()

        serializer = DropoffSerializer(new_dropoff, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single dropoff date
        Returns:
            Response -- JSON serialized dropoff instance
        """
        try:
            dropoff = Dropoff.objects.get(pk=pk)
            serializer = DropoffSerializer(dropoff, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single dropoff
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            single_dropoff = Dropoff.objects.get(pk=pk)
            single_dropoff.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Dropoff.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests Dropoff
        Returns:
            Response -- JSON serialized list of Dropoffs
        """
        all_dropoffs = Dropoff.objects.all()


        dropoff_date = self.request.query_params.get('donator', None)
        if dropoff_date is not None:
            all_dropoffs = all_dropoffs.filter(donator__id=dropoff_date)

        serializer = DropoffSerializer(
            all_dropoffs, many=True, context={'request': request})
        return Response(serializer.data)