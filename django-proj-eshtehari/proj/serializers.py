from rest_framework import serializers
# from .models import *
from .models import *
import uuid

# from rest_framework.reverse import reverse

class NewsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()  # Use UUIDField for UUID primary key
    url = serializers.CharField()
    head = serializers.CharField()
    author = serializers.CharField()
    category = serializers.CharField()
    date = serializers.CharField()
    tags = serializers.CharField()
    text = serializers.CharField()
    summary = serializers.CharField()
    hashtags  = serializers.CharField()
    keywords  = serializers.CharField()

    # def create(self, validated_data):
    #     return NewsModel(**validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    class Meta:
        model = NewsModel
        fields = "__all__"


# class AuthorSerializer(serializers.Serializer):
#     author = serializers.CharField()
