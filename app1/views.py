import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .models import Watch, StreamingPlatform, Review


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Querysets
        reviews_qs = Review.objects.select_related('watchlist', 'watchlist__platform')
        watchlist_qs = Watch.objects.all()
        platforms_qs = StreamingPlatform.objects.all()

        # Convert to DataFrames
        reviews_df = pd.DataFrame(list(reviews_qs.values('id', 'ratings', 'watchlist__title', 'watchlist__platform__name','like')))
        watchlist_df = pd.DataFrame(list(watchlist_qs.values('id', 'title')))
        platforms_df = pd.DataFrame(list(platforms_qs.values('id', 'name')))

        # Compute Stats
        avg_ratings = reviews_df.groupby('watchlist__title')['ratings'].mean().reset_index().rename(columns={
            'watchlist__title': 'title',
            'ratings': 'avg_rating'
        })

        most_reviewed = reviews_df['watchlist__title'].value_counts().reset_index().rename(columns={
            'index': 'title',
            'watchlist__title': 'num_reviews'
        }).head(5)

        reviews_per_platform = reviews_df['watchlist__platform__name'].value_counts().reset_index().rename(columns={
            'index': 'platform',
            'watchlist__platform__name': 'total_reviews'
        })
        
        # Get trending shows based on likes
        trending = reviews_df[reviews_df['like'] == True] \
            .groupby('watchlist__title') \
            .size() \
            .reset_index(name='like_count') \
            .sort_values(by='like_count', ascending=False) \
            .head(5)

        # Convert to list of dicts for JSON response
        trending_shows = trending.rename(columns={
            'watchlist__title': 'title',
            'like_count': 'likes'
        }).to_dict(orient='records')

        # Response
        response = {
            "table_data": {
                "total_movies": watchlist_df.shape[0],
                "total_reviews": reviews_df.shape[0],
                "total_users": User.objects.count(),
                "total_platforms": platforms_df.shape[0],
            },
            "chart_data": {
                "avg_ratings": avg_ratings.to_dict(orient='records'),
                "most_reviewed": most_reviewed.to_dict(orient='records'),
                "reviews_per_platform": reviews_per_platform.to_dict(orient='records'),
                "trending_shows": trending_shows, 
            }
        }

        return Response(response)

