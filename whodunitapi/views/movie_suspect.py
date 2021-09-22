from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.contrib.auth.models import User 
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Suspect, MovieNight, MovieSuspect, Player

class MovieSuspectView(ViewSet):
    """WHODUNIT MovieSuspects"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized suspect instance
        """

        # Uses the token passed in the `Authorization` header
        player = Player.objects.get(user=request.auth.user)
        
        movie_suspect = MovieSuspect()
        movie_suspect.player = player
        suspect = Suspect.objects.get(pk=request.data["suspectId"])
        movie_suspect.suspect = suspect
        
        movie_night = MovieNight.objects.get(pk=request.data["movieNightId"])
        movie_suspect.movie_night = movie_night

        try:
            movie_suspect.save()
            serializer = MovieSuspectSerializer(movie_suspect, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single suspect
        Returns:
            Response -- JSON serialized suspect instance
        """
        try:
            movie_suspect = MovieSuspect.objects.get(pk=pk)
            serializer = MovieSuspectSerializer(movie_suspect, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a suspect
        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)

        movie_suspect = MovieSuspect().objects.get(pk=pk)
        suspect = Suspect.objects.get(pk=request.data["suspectId"])
        movie_suspect.suspect = suspect
        movie_night = MovieNight.objects.get(pk=request.data["movieNightId"])
        movie_suspect.movie_night = movie_night
        movie_night.player = player        
        movie_suspect.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single suspect
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            movie_suspect = MovieSuspect.objects.get(pk=pk)
            movie_suspect.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MovieSuspect.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to suspects resource
        Returns:
            Response -- JSON serialized list of suspects
        """
        player = Player.objects.get(user=request.auth.user)
        movie_suspects = MovieSuspect.objects.all()

        player = self.request.query_params.get('type', None)
        if player is not None:
            movie_suspects = movie_suspects.filter(player__id=player)

        suspect = self.request.query_params.get('type', None)
        if suspect is not None:
            movie_suspects = movie_suspects.filter(suspect__id=suspect)
        
        movie_night = self.request.query_params.get('type', None)
        if movie_night is not None:
            movie_suspects = movie_suspects.filter(movie_night__id=movie_night)


        serializer = MovieSuspectSerializer(
            movie_suspects, many=True, context={'request': request})
        return Response(serializer.data)

class MovieSuspectUserSerializer(serializers.ModelSerializer):
    """JSON serializer for movie_night organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class MovieSuspectPlayerSerializer(serializers.ModelSerializer):
    """JSON serializer for movie_night organizer"""
    user = MovieSuspectUserSerializer(many=False)

    class Meta:
        model = Player
        fields = ['user']

class MovieSuspectSerializer(serializers.ModelSerializer):
    """JSON serializer for movieNights"""
    # creator = MovieSuspectPlayerSerializer(many=False)
    
    class Meta:
        model = MovieSuspect
        fields = ('id', 'creator','suspect', 'movie_night')
        depth = 3
        