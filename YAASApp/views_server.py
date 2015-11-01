from rest_framework.views import APIView

from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from YAASApp.models import Auction
from YAASApp.serializers import AuctionSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


#@csrf_exempt
@api_view(['GET', 'PUT'])
@renderer_classes([JSONRenderer,])
def auction_list(request):
    if request.method == 'GET':
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
        #print serializer.data
        #return JSONResponse(serializer.data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AuctionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

#@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def auction_detail(request, pk):
    """
    Retrieve, update or delete a blog.
    """
    try:
        auction = Auction.objects.get(pk=pk)
    except Auction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AuctionSerializer(auction)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
        data = request.data
        print request.data
        serializer = AuctionSerializer(auction, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        auction.delete()
        return HttpResponse(status=204)


class AuthView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = AuctionSerializer(blog)
        return Response(serializer.data)