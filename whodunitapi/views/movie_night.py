"""View module for handling requests about movieNights"""
from django.contrib.auth.models import User #pylint:disable=(imported-auth-user)
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Movie, MovieNight, Player



class MovieNightView(ViewSet):
    """WHODUNIT MovieNights"""

    def create(self, request):
        """Handle POST operations for movie_nights
        Returns:
            Response -- JSON serialized movieNight instance
        """
        player = Player.objects.get(user=request.auth.user)

        movie_night = MovieNight()
        movie_night.creator = player
        movie_night.title = request.data["title"]
        movie_night.date = request.data["date"]
        movie_night.time = request.data["time"]
        movie_night.description = request.data["description"]    

        movie = Movie.objects.get(pk=request.data["movie"])
        movie_night.movie = movie

        try:
            movie_night.save()
            serializer = MovieNightSerializer(movie_night, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single movie_night
        Returns:
            Response -- JSON serialized movie instance
        """
        try:
            movie_night = MovieNight.objects.get(pk=pk)
            serializer = MovieNightSerializer(movie_night, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an movie_night
        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)

        movie_night = MovieNight().objects.get(pk=pk)
        movie_night.title = request.data["title"]
        movie_night.date = request.data["date"]
        movie_night.time = request.data["time"]
        movie_night.description = request.data["description"]
        movie_night.creator = player

        movie = Movie.objects.get(pk=request.data["movie"])
        movie_night.movie = movie
        movie_night.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single movie
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            movie_night = MovieNight.objects.get(pk=pk)
            movie_night.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MovieNight.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to movieNights resource
        Returns:
            Response -- JSON serialized list of movieNights ojb to json
        """
        # Get the current authenticated user
        player = Player.objects.get(user=request.auth.user)
        movie_nights = MovieNight.objects.all()

        # Set the `joined` property on every movieNight
        for movie_night in movie_nights:
            # Check to see if the player is in the attendees list on the movieNight. set from the setter
            movie_night.joined = player in movie_night.attendees.all()

        # Support filtering movie_night by movie
        movie = self.request.query_params.get('movieId', None)
        if movie is not None:
            movie_night = movie_nights.filter(movie__id=type)

        serializer = MovieNightSerializer(
            movie_nights, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing players signing up for movieNights"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up
        player = Player.objects.get(user=request.auth.user) #gets the user from the token

        try:
            # Handle the case if the client specifies a movie
            # that doesn't exist
            movie_night = MovieNight.objects.get(pk=pk)
        except MovieNight.DoesNotExist:
            return Response(
                {'message': 'MovieNight does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A player wants to sign up for an movie_night
        if request.method == "POST":
            try:
                # Using the attendees field on the movie_night makes it simple to add a player to the movie_night
                # .add(player) will insert into the join table a new row the player_id and the movie_night_id
                movie_night.attendees.add(player)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined movie_night
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the player from the attendees list
                # The method deletes the row in the join table that has the player_id and movie_night_id
                movie_night.attendees.remove(player)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})

class MovieNightUserSerializer(serializers.ModelSerializer):
    """JSON serializer for movie_night organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class MovieNightPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for movie_night organizer"""
    user = MovieNightUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user']

class MovieSerializer(serializers.ModelSerializer):
    """JSON serializer for movies"""
    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'number_of_players', 'player', 'director')

class MovieNightSerializer(serializers.ModelSerializer):
    """JSON serializer for movieNights"""
    creator = MovieNightPlayerSerializer(many=False)
    movie = MovieSerializer(many=False)

    class Meta:
        model = MovieNight
        fields = ('id', 'title', 'date', 'time', 'description', 'creator', 'movie', 'attendees', 'joined')
        depth = 2
