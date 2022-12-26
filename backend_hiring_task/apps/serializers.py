from rest_framework import serializers

from .models import Apps, Dicty


class DictySerializer(serializers.ModelSerializer):

    class Meta:
        model = Dicty
        fields = "__all__"


class AppsSerializer(serializers.ModelSerializer):
    envs = DictySerializer(read_only=True, many=True)

    class Meta:
        model = Apps
        fields = ['id', 'name', 'image', 'envs', 'command']
        depth = 2



