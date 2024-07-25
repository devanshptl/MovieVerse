from .serializers import *
from app1.models import *
from app1.api.permissions import *
from app1.api.throttling import *
from app1.api.paginations import *
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import filters



# Create your views here.

class WatchlistAV(generics.ListCreateAPIView):
     pagination_class = Watchpages
     permission_classes = [AuthorORReadOnly]
     throttle_classes = [AnonRateThrottle]
     serializer_class = WatchSerializers
     queryset = Watch.objects.all()
     filter_backends = [filters.SearchFilter]
     search_fields = ['title', 'platform__name']

class WatchdetailsAV(APIView):
    permission_classes = [AuthorORReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get(self, request ,pk):
        movie = Watch.objects.get(id = pk)
        serializer = WatchSerializers(movie)
        return Response(serializer.data)
    
    def put(self, request ,pk):
          movie = Watch.objects.get(id = pk)
          serializer = WatchSerializers(movie,data= request.data)
          if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
          else:
             return Response(serializer.errors)
        
    def delete(self, reuqest, pk):
          movie = Watch.objects.get(id = pk)
          movie.delete()
          return Response(status= status.HTTP_204_NO_CONTENT)    
      
class StreamingPlatformListAV(APIView):
    permission_classes = [AuthorORReadOnly]
    throttle_classes = [AnonRateThrottle]
    
    def get(self, request):
        platform = StreamingPlatform.objects.all()
        serializer = StreameSerializers(platform, many = True) # context={'request': request}  for hyperlink relationship
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreameSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)
    

class StreamingPlatformdetailsAV(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    
    def get(self, request, pk):
        platform = StreamingPlatform.objects.get(id = pk)
        serializer = StreameSerializers(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = StreamingPlatform.objects.get(id = pk)
        serializer = StreameSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else :
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        platform = StreamingPlatform.objects.get(id = pk)
        platform.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)
    
class CategoryListAV(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = WatchSerializers
    permission_classes = [AuthorORReadOnly]
    
    def get_queryset(self):
        name = self.kwargs['name']
        return Watch.objects.filter(category__name = name)
    
            
class ReviewlistAV(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username', 'watchlist__title']
    
    serializer_class = ReviewSerializers
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)
    

class ReviewDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle,AnonRateThrottle]
    permission_classes = [ReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    
    
class ReviewCreate(generics.CreateAPIView): 
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    serializer_class = ReviewSerializers
    
    def get_queryset(self):
        return Review.objects.all() 
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Watch.objects.get(pk = pk)
        r_user = self.request.user
        
        if movie.avg_rating == 0:
            movie.avg_rating = serializer.validated_data['ratings']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['ratings'] )/2
            
        movie.total_reviews = movie.total_reviews + 1
        movie.save()
        
        
        serializer.save(watchlist = movie, user = r_user)
    

class ReviewUser(generics.ListAPIView):
    serializer_class  = ReviewSerializers
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(user__username = username)
    