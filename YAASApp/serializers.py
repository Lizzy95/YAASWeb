from django.forms import widgets
from rest_framework import serializers
from YAASApp.models import Auction

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ('idItem',
                  'titleAuc',
                  'posted',
                  'deadLine',
                  'content',
                  'minPrice')
