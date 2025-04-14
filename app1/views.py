# app1/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from taggit.models import Tag
from collections import Counter
from app1.models import Watch, Review
from .api.serializers import WatchSerializers  # assuming this already exists


class RecommendedMoviesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_reviews = Review.objects.filter(user=user, like=True).select_related(
            "watch"
        )
        liked_movies = [review.watch for review in liked_reviews]

        # Step 1: Unique liked tags
        liked_tags = set()
        for movie in liked_movies:
            liked_tags.update(movie.tags.names())

        if not liked_tags:
            return Response({"message": "No liked movies with tags found."}, status=204)

        # Step 2: Score other movies by tag overlap
        liked_movie_ids = [movie.id for movie in liked_movies]
        all_movies = Watch.objects.exclude(id__in=liked_movie_ids)
        scored_movies = []

        for movie in all_movies:
            movie_tags = set(movie.tags.names())
            common_tag_count = len(movie_tags & liked_tags)
            if common_tag_count > 0:
                scored_movies.append((movie, common_tag_count))

        # Step 3: Return top 5 sorted by similarity
        scored_movies.sort(key=lambda x: x[1], reverse=True)
        top_5_movies = [item[0] for item in scored_movies[:5]]
        serialized = WatchSerializers(top_5_movies, many=True)

        return Response(serialized.data)
