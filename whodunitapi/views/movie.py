"""View module for handling requests about movies"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from whodunitapi.models import Movie, Genre, Player, Suspect


class MovieView(ViewSet):
    """WHODUNIT movies"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized movie instance
        """

        # Uses the token passed in the `Authorization` header
        player = Player.objects.get(user=request.auth.user)

        # Create a new Python instance of the Movie class
        # and set its properties from what was sent in the
        # body of the request from the client.
        movie = Movie()
        player = Player.objects.get(pk=request.data["playerId"])
        movie.player = player
        movie.name = request.data["name"]
        movie.year = request.data["year"]
        movie.description = request.data["description"]
        movie.number_of_players = request.data["numberOfPlayers"]
        movie.director = request.data["director"]
        movie.rating = request.data["rating"]

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `genreId` in the body of the request.
        genre = Genre.objects.get(pk=request.data["genreId"])
        movie.genre = genre

        suspect = Suspect.objects.get(pk=request.data["suspectId"])
        movie.suspect = suspect
        

        # Try to save the new movie to the database, then
        # serialize the movie instance as JSON, and send the
        # JSON as a response to the client request
        try:
            movie.save()
            serializer = MovieSerializer(movie, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single movie
        Returns:
            Response -- JSON serialized movie instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/movies/2
            #
            # The `2` at the end of the route becomes `pk`
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie, context={'request': request})
            return Response(serializer.data)

        except Movie.DoesNotExist as ex: #from models.model
            return Response(ex.args[0], status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a movie
        Returns:
            Response -- Empty body with 204 no content status code
        """
        player = Player.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Movie, get the movie record
        # from the database whose primary key is `pk`
        # if  http://localhost:8000/movies/3, the route parameter of 3 becomes the value of the pk parameter below.
        movie = Movie.objects.get(pk=pk)
        player = Player.objects.get(pk=request.data["playerId"])
        movie.player = player
        movie.name = request.data["name"]
        movie.year = request.data["year"]
        movie.description = request.data["description"]
        movie.number_of_players = request.data["numberOfPlayers"]
        movie.director = request.data["director"]
        movie.rating = request.data["rating"]
        genre = Genre.objects.get(pk=request.data["genreId"])
        movie.genre = genre
        
        suspect = Suspect.objects.get(pk=request.data["suspectId"])
        movie.suspect = suspect
        movie.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single movie
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Movie.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to movies resource
        Returns:
            Response -- JSON serialized list of movies
        """
        # Get all movie records from the database
        movies = Movie.objects.all()

        # Support filtering movies by type
        #    http://localhost:8000/movies?type=1
        #
        # That URL will retrieve all movies
        player = self.request.query_params.get('type', None)
        if player is not None:
            movies = movies.filter(player__id=player)
        
        genre = self.request.query_params.get('type', None)
        if genre is not None:
            movies = movies.filter(genre__id=genre)

        suspect = self.request.query_params.get('type', None)
        if suspect is not None:
            movies = movies.filter(suspect__id=suspect)


        serializer = MovieSerializer(
            movies, many=True, context={'request': request})
        return Response(serializer.data)

class MovieSerializer(serializers.ModelSerializer):
    """JSON serializer for movies
    Arguments:
        serializer type
    """
    class Meta:
        model = Movie
        fields = ('id', 'name', 'year', 'player', 'genre', 'description', 'rating','number_of_players', 'director', 'suspect' )
        depth = 1
