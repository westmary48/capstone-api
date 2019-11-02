from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from sizeyourdriveapi.models import Item
from sizeyourdriveapi.models import Donator
from sizeyourdriveapi.models import ItemCategory
from sizeyourdriveapi.models import ItemDonationbox
from sizeyourdriveapi.models import DonationBox
from .donator import DonatorSerializer



class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for item
    Arguments:
        serializers
    """
    donator = DonatorSerializer(many=False)
    class Meta:
        model = Item
        url = serializers.HyperlinkedIdentityField(
            view_name='item',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'size', 'description', 'quantity', 'created_date',  'donator', 'item_category')
        depth = 2


class Items(ViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized item instance
        """
        new_item = Item()
        new_item.name = request.data["name"]
        new_item.size = request.data["size"]
        new_item.description = request.data["description"]
        new_item.quantity = request.data["quantity"]
        new_item.created_date = request.data["created_date"]

        donator = Donator.objects.get(user=request.auth.user)
        new_item.donator = donator

        item_category = ItemCategory.objects.get(pk=request.data["item_category_id"])
        new_item.item_category = item_category

        new_item.save()

        serializer = ItemSerializer(new_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item
        Returns:
            Response -- JSON serialized item instance
        """
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a item attraction
        Returns:
            Response -- Empty body with 204 status code
        """
        item = Item.objects.get(pk=pk)
        item.quantity = request.data["quantity"]
        item.created_date = request.data["created_date"]
        item.name = request.data["name"]
        item.description = request.data["description"]
        item.size = request.data["size"]

        donator = Donator.objects.get(user=request.auth.user)
        item.donator = donator


        item_category = ItemCategory.objects.get(pk=request.data["item_category_id"])
        item.item_category = item_category
        item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            item = Item.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to item resource
        Returns:
            Response -- JSON serialized list of item
        """

        # items = Item.objects.all()
        items = Item.objects.all()


        # Support filtering attractions by area id
        category = self.request.query_params.get('category', None)
        item_donator = self.request.query_params.get('donator', None)
        quantity = self.request.query_params.get('quantity', None)
        name = self.request.query_params.get('name', None)

        if name is not None:
            items = items.filter(name__iexact=name, quantity__gte=1)

        if category is not None:
            items = items.filter(item_category__id=category, quantity__gte=1)

        if item_donator is not None:
            donator_items = Donator.objects.get(user=request.auth.user).items.all()
            items = donator_items

        if quantity is not None:
            quantity = int(quantity)
            items = items.filter(quantity__gte=1).order_by("-created_date")[:quantity]


        serializer = ItemSerializer(items, many=True, context={'request': request})

        return Response(serializer.data)