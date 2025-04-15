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
