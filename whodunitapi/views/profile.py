"""View module for handling requests about park areas"""
from django.contrib.auth.models import User #pylint:disable=imported-auth-user
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import MovieNight, Player, Movie


class Profile(ViewSet):
    """Player can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource
        Returns:
            Response -- JSON representation of user info and movie_nights
        """
        player = Player.objects.get(user=request.auth.user)
        movie_nights = MovieNight.objects.filter(attendees=player) #checking if there are movies in the attendees list

        movie_nights = MovieNightSerializer(
            movie_nights, many=True, context={'request': request})
        player = PlayerSerializer(
            player, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["player"] = player.data
        profile["movie_nights"] = movie_nights.data

        return Response(profile)

#restricts passing user data like passwords

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for player's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
class PlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for players"""
    user = UserSerializer(many=False)

    class Meta:
        model = Player
        fields = ('user', 'bio')

class MovieSerializer(serializers.ModelSerializer):
    """JSON serializer for movies"""
    class Meta:
        model = Movie
        fields = ('name')

class MovieNightSerializer(serializers.ModelSerializer):
    """JSON serializer for movie_nights"""
    movie = MovieSerializer(many=False)

    class Meta:
        model = MovieNight
        fields = ('id', 'movie', 'description', 'date', 'time')
