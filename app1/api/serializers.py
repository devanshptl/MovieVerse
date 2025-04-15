from rest_framework import serializers
from app1.models import *
from taggit.serializers import TagListSerializerField, TaggitSerializer


class ReviewSerializers(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ("watchlist",)


class WatchSerializers(serializers.ModelSerializer):

    # Show_reviews = ReviewSerializers(many = True, read_only = True)
    platform = serializers.CharField(source="platform.name")
    category = serializers.CharField(source="category.name")
    tags = TagListSerializerField()

    class Meta:
        model = Watch
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    category = WatchSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class StreameSerializers(serializers.ModelSerializer):

    watchlist = WatchSerializers(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = "__all__"


class LikeSerializers(serializers.ModelSerializer):
    watchlist = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ["watchlist"]

    def get_watchlist(self, obj):
        return obj.watchlist.title
    
class TrendingShowSerializer(serializers.Serializer):
    title = serializers.CharField()
    like_count = serializers.IntegerField()
    
    
class UserFollowPlatformSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(write_only=True)

    class Meta:
        model = UserFollowPlatform
        fields = ['platform_name', 'is_following']

    def create(self, validated_data):
        platform_name = validated_data.get('platform_name')
        platform = StreamingPlatform.objects.get(name=platform_name)
        user = self.context['request'].user  
        
        user_follow = UserFollowPlatform.objects.filter(user=user, platform=platform).first()
        
        if user_follow:
            user_follow.is_following = validated_data.get('is_following', False)
            user_follow.save()
        else:
            user_follow = UserFollowPlatform.objects.create(
                user=user,
                platform=platform,
                is_following=validated_data.get('is_following', False)
            )
        return user_follow
    
class FollowedPlatformSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform')
    
    class Meta:
        model = UserFollowPlatform
        fields = ['platform_name', 'is_following']
