from rest_framework import serializers

class URLSerializer(serializers.Serializer):
    url = serializers.URLField()

class ResultSerializer(serializers.Serializer):
    is_phishing = serializers.BooleanField()
    confidence = serializers.FloatField()