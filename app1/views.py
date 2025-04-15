import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .models import Watch, StreamingPlatform, Review, UserFollowPlatform


class AdminStatsView(APIView):
    # permission_classes = [IsAdminUser]

    def get(self, request):
        # Querysets
        reviews_qs = Review.objects.select_related('watchlist', 'watchlist__platform')
        watchlist_qs = Watch.objects.all()
        platforms_qs = StreamingPlatform.objects.all()
        follows_qs = UserFollowPlatform.objects.filter(is_following=True).select_related('platform')

        # Convert to DataFrames
        reviews_df = pd.DataFrame(list(reviews_qs.values('id', 'ratings', 'watchlist__title', 'watchlist__platform__name', 'like')))
        watchlist_df = pd.DataFrame(list(watchlist_qs.values('id', 'title')))
        platforms_df = pd.DataFrame(list(platforms_qs.values('id', 'name')))
        follows_df = pd.DataFrame(list(follows_qs.values('platform__name')))

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

        trending = reviews_df[reviews_df['like'] == True] \
            .groupby('watchlist__title') \
            .size() \
            .reset_index(name='like_count') \
            .sort_values(by='like_count', ascending=False) \
            .head(5)

        trending_shows = trending.rename(columns={
            'watchlist__title': 'title',
            'like_count': 'likes'
        }).to_dict(orient='records')

        # Most followed platforms
        if not follows_df.empty:
            most_followed = follows_df['platform__name'].value_counts().reset_index().rename(columns={
                'index': 'platform',
                'platform__name': 'follower_count'
            }).head(5).to_dict(orient='records')
        else:
            most_followed = []

        # Final Response
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
                "most_followed_platforms": most_followed,
            }
        }

        return Response(response)