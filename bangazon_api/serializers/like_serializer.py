from rest_framework import serializers
from bangazon_api.models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product', 'user')
        depth = 1
