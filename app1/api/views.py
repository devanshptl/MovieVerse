from .serializers import *
from app1.models import *
from app1.api.permissions import *
from app1.api.throttling import *
from app1.api.paginations import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import *
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import filters
from django.db.models import Count


# Create your views here.


class WatchlistAV(generics.ListCreateAPIView):
    pagination_class = Watchpages
    permission_classes = [AuthorORReadOnly]
    throttle_classes = [AnonRateThrottle]
    serializer_class = WatchSerializers
    queryset = Watch.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "platform__name"]


class WatchdetailsAV(APIView):
    permission_classes = [AuthorORReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request, pk):
        movie = Watch.objects.get(id=pk)
        serializer = WatchSerializers(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = Watch.objects.get(id=pk)
        serializer = WatchSerializers(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, reuqest, pk):
        movie = Watch.objects.get(id=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamingPlatformListAV(APIView):
    permission_classes = [AuthorORReadOnly]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        platform = StreamingPlatform.objects.all()
        serializer = StreameSerializers(
            platform, many=True
        )  # context={'request': request}  for hyperlink relationship
        return Response(serializer.data)

    def post(self, request):
        serializer = StreameSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamingPlatformdetailsAV(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, pk):
        platform = StreamingPlatform.objects.get(id=pk)
        serializer = StreameSerializers(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamingPlatform.objects.get(id=pk)
        serializer = StreameSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        platform = StreamingPlatform.objects.get(id=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListAV(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle]
    serializer_class = WatchSerializers
    permission_classes = [AuthorORReadOnly]

    def get_queryset(self):
        name = self.kwargs["name"]
        return Watch.objects.filter(category__name=name)


class ReviewlistAV(generics.ListAPIView):
    throttle_classes = [AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user__username", "watchlist__title"]

    serializer_class = ReviewSerializers

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)


class ReviewDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
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
        pk = self.kwargs.get("pk")
        movie = Watch.objects.get(pk=pk)
        r_user = self.request.user

        if movie.avg_rating == 0:
            movie.avg_rating = serializer.validated_data["ratings"]
        else:
            movie.avg_rating = (
                movie.avg_rating + serializer.validated_data["ratings"]
            ) / 2

        movie.total_reviews = movie.total_reviews + 1
        movie.save()

        serializer.save(watchlist=movie, user=r_user)


class ReviewUser(generics.ListAPIView):
    serializer_class = ReviewSerializers

    def get_queryset(self):
        username = self.kwargs["username"]
        return Review.objects.filter(user__username=username)


class LikedReviewsView(generics.ListAPIView):
    serializer_class = LikeSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user, like=True)


class RecommendedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_reviews = Review.objects.filter(user=user, like=True).select_related(
            "watchlist"
        )
        liked_movies = [review.watchlist for review in liked_reviews]

        liked_tags = set()
        for movie in liked_movies:
            liked_tags.update(movie.tags.names())

        if not liked_tags:
            return Response({"message": "No liked movies with tags found."}, status=204)

        liked_movie_ids = [movie.id for movie in liked_movies]
        all_movies = Watch.objects.exclude(id__in=liked_movie_ids)
        scored_movies = []

        for movie in all_movies:
            movie_tags = set(movie.tags.names())
            common_tag_count = len(movie_tags & liked_tags)
            if common_tag_count > 0:
                scored_movies.append((movie, common_tag_count))

        scored_movies.sort(key=lambda x: x[1], reverse=True)
        top_5_movies = [item[0] for item in scored_movies[:5]]
        serialized = WatchSerializers(top_5_movies, many=True)

        return Response(serialized.data)
    
class TrendingShowsView(APIView):
    def get(self, request):
        # Aggregate trending data
        trending_data = (
            Review.objects.filter(like=True)
            .values('watchlist__title')  # this will be the dictionary key
            .annotate(like_count=Count('id'))
            .order_by('-like_count')[:5]
        )
        
        # Convert 'watchlist__title' key to 'title' for consistency with the serializer
        trending_data = [
            {'title': item['watchlist__title'], 'like_count': item['like_count']}
            for item in trending_data
        ]
        
        # Serialize the data
        serializer = TrendingShowSerializer(trending_data, many=True)
        
        # Return response
        return Response(serializer.data, status=status.HTTP_200_OK)
