from rest_framework import serializers
from .models import Job, Profile, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class JobSerializer(serializers.ModelSerializer):
    skills = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'skills', 'created_at']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'skills', 'resume']