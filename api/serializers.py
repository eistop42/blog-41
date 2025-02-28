from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    title = serializers.CharField()
    text = serializers.CharField(max_length=200)
    category = serializers.CharField()