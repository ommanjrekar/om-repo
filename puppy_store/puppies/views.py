from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Puppy
from .serializers import PuppySerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response 
from django.http import Http404
from rest_framework.generics import GenericAPIView 
from rest_framework import mixins
from rest_framework import generics


class 


'''
#####GenericViews
class Pagination(PageNumberPagination):
    page_size = 2

class Puppy_list(generics.ListCreateAPIView):
    queryset = Puppy.objects.all().order_by('id')
    serializer_class = PuppySerializer
    pagination_class = Pagination

class PuppyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Puppy.objects.all()
    serializer_class = PuppySerializer
'''
'''
#####Using Mixins
class Puppy_list(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Puppy.objects.all()
    serializer_class = PuppySerializer
    
    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

class PuppyDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Puppy.objects.all()
    serializer_class = PuppySerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
'''
'''
#####Using APIView
class Puppy_list(APIView):
    def get(self, request):
        puppy = Puppy.objects.all()
        serializer = PuppySerializer(puppy, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PuppySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PuppyDetail(APIView):
    def get_object(self,pk):
        try:
            return Puppy.objects.get(pk=pk)
        except Puppy.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        puppy = self.get_object(pk)
        serializer = PuppySerializer(puppy)
        return Response(serializer.data)

    def put(self, request, pk):
        puppy = self.get_object(pk)
        serializer = PuppySerializer(puppy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        puppy = self.get_object(pk)
        puppy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
'''
#####Using Viewset
class Pagination(PageNumberPagination):
    page_size = 2

class PuppyViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Puppy.objects.all()
    serializer_class = PuppySerializer
    pagination_class = LimitOffsetPagination
'''
'''
@api_view(['GET', 'PUT', 'DELETE'])
def get_delete_update_puppy(request, pk):
    try:
        puppy = Puppy.objects.get(pk=pk)
    except Puppy.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    #get details of single puppy
    if request.method == 'GET':
        serializer = PuppySerializer(puppy)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PuppySerializer(puppy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        puppy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def get_post_puppy(request):
    #get all puppies
    if request.method == 'GET':
        puppies = Puppy.objects.all()
        serializer = PuppySerializer(puppies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            'name' : request.data.get('name'),
            'age' : int(request.data.get('age')),
            'breed' : request.data.get('breed'),
            'color' : request.data.get('color'),
        }
        serializer = PuppySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
'''
