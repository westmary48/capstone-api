"""View module for handling requests about donation boxes"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sizeyourdriveapi.models import DonationBox, Dropoff, Donator
from .donator import DonatorSerializer



class DonationBoxSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for donationbox
    Arguments:
        serializers
    """

    donator = DonatorSerializer(many=False)

    class Meta:
        model = DonationBox
        url = serializers.HyperlinkedIdentityField(
            view_name='donationbox',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_date', 'dropoff', "donator")
        depth = 1


class DonationBoxes(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized DonationBox instance
        """
        newdonationbox = DonationBox()
        newdonationbox.created_date = request.data["created_date"]
        donator = Donator.objects.get(id=request.data["donator_id"])
        newdonationbox.donator = donator
        newdonationbox.save()

        serializer = DonationBoxSerializer(newdonationbox, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for donationbox
        Returns:
            Response -- JSON serialized donationbox
        """
        try:
            donationbox = DonationBox.objects.get(pk=pk)
            serializer = DonationBoxSerializer(donationbox, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a donationbox
        Returns:
            Response -- Empty body with 204 status code
        """
        donated_items = set()
        donationbox = DonationBox.objects.get(pk=pk)
        dropoff = Dropoff.objects.get(pk=request.data["dropoff"])
        donationbox.dropoff = dropoff
        donationbox.save()
        if donationbox.dropoff is not "NULL":
            clothing_items = donationbox.invoiceline.all()

            for di in clothing_items:
                donated_items.add(di.item)

            items = list(donated_items)

            for p in items:
                num_sold = p.item.filter(donationbox=donationbox).count()
                p.quantity = p.new_inventory(num_sold)
                p.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single donationbox
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            donationbox = DonationBox.objects.get(pk=pk)
            donationbox.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except DonationBox.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to donationboxes resource
        Returns:
            Response -- JSON serialized list of donation boxes
        """
        donationboxes = DonationBox.objects.all()

        donator = self.request.query_params.get('donator_id', None)
        complete = self.request.query_params.get('complete', None)
        dropoff = self.request.query_params.get('dropoff_id', None)
        if donator is not None:
            if complete == "0":
                donationboxes = donationboxes.filter(donator__id=donator, dropoff__id__isnull=True)
            if complete == "1":
                donationboxes = donationboxes.filter(donator__id=donator, dropoff__id__isnull=False)

        if dropoff is not None:
            donationboxes = donationboxes.filter(dropoff__id=dropoff)
        if complete is not None:
            print("hello")
            if complete == "1":
                donationboxes = donationboxes.filter(dropoff__id__isnull=False)
            elif complete == "0":
                donationboxes = donationboxes.filter(dropoff__id__isnull=True)

        serializer = DonationBoxSerializer(
            donationboxes, many=True, context={'request': request})
        return Response(serializer.data)