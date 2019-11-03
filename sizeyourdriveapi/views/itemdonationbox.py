
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from sizeyourdriveapi.models import ItemDonationbox, DonationBox, Item, Donator
from .item import ItemSerializer
from .donationbox import DonationBoxSerializer
import datetime


class ItemDonationBoxSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for item donation box
    Arguments:
        serializers
    """
    item = ItemSerializer(many=False)
    class Meta:
        model = ItemDonationbox
        url = serializers.HyperlinkedIdentityField(
            view_name='itemdonationbox',
            lookup_field='id'
        )
        fields = ('id', 'url', 'donationbox', 'item', 'quantity')
        depth = 2

class ItemDonationBoxes(ViewSet):

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized item donation box instance
        """
        new_item_donationbox = ItemDonationbox()
        new_item_donationbox.item = Item.objects.get(pk=request.data["item"])
        new_item_donationbox.quantity = request.data["quantity"]
        donator = Donator.objects.get(user=request.auth.user)
        try:
            newdonationbox = DonationBox.objects.get(donator=donator, dropoff__isnull=True)
        except DonationBox.DoesNotExist:
            newdonationbox = DonationBox()
            newdonationbox.created_date = datetime.date.today()
            newdonationbox.donator = donator
            newdonationbox.save()


        new_item_donationbox.donationbox = newdonationbox
        new_item_donationbox.save()


        serializer = ItemDonationBoxSerializer(new_item_donationbox, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests
        Returns:
            Response -- JSON serialized instance
        """
        try:
            item_donationbox = ItemDonationbox.objects.get(pk=pk)
            serializer = ItemDonationBoxSerializer(item_donationbox, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests
        Returns:
            Response -- Empty body with 204 status code
        """
        new_item_donationbox = ItemDonationbox.objects.get(pk=pk)
        new_item_donationbox.quantity = request.data["quantity"]
        new_item_donationbox.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            item_donationbox = ItemDonationbox.objects.get(pk=pk)
            item_donationbox.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except item_donationbox.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to ItemDonationBoxes resource
        Returns:
            Response -- JSON serialized list of ItemDonationBoxes
        """
        ItemDonationboxes = ItemDonationbox.objects.all()

        itemId = self.request.query_params.get('item_id', None)
        donationbox = self.request.query_params.get('donationbox_id', None)
        if donationbox is not None:
            ItemDonationboxes = ItemDonationboxes.filter(donationbox__id=donationbox)


        if itemId is not None:
            ItemDonationboxes = ItemDonationboxes.filter(item__id=itemId)

        serializer = ItemDonationBoxSerializer(
            ItemDonationboxes, many=True, context={'request': request})
        return Response(serializer.data)