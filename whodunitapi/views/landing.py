from django.contrib.auth.models import User #pylint:disable=imported-auth-user
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Player


class Landing(ViewSet):
    """Player can see landing information"""

    def list(self, request):
        """Handle GET requests to landing resource
        Returns:
            Response -- JSON representation of user info and movie_nights
        """
        player = Player.objects.get(user=request.auth.user)

        player = PlayerSerializer(
            player, many=False, context={'request': request})
        landing = {}
        landing["player"] = player.data
        return Response(landing)

class UserSerializer(serializers.ModelSerializer):
        """JSON serializer for player's related Django user"""
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email', 'username', 'is_staff']


class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for players"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['id', 'user', 'bio']