from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Suspect, Guilty, Player, Movie

class SuspectView(ViewSet):
    """WHODUNIT Suspects"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized suspect instance
        """

        # Uses the token passed in the `Authorization` header
        player = Player.objects.get(user=request.auth.user)
        
        suspect = Suspect()
        suspect.player = player
        suspect.name = request.data["name"]
        suspect.description = request.data["description"]
        guilty = Guilty.objects.get(pk=request.data["guiltyId"])
        suspect.guilty = guilty
        movie = Movie.objects.get(pk=request.data["movieId"])
        suspect.suspect_image_url = request.data["suspectImageUrl"]
        suspect.movie = movie
        

        try:
            suspect.save()
            serializer = SuspectSerializer(suspect, context={'request': request})
            return Response(serializer.data)


        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single suspect
        Returns:
            Response -- JSON serialized suspect instance
        """
        try:
            
            suspect = Suspect.objects.get(pk=pk)
            serializer = SuspectSerializer(suspect, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a suspect
        Returns:
            Response -- Empty body with 204 status code
        """
        player = Player.objects.get(user=request.auth.user)
        suspect = Suspect.objects.get(pk=pk)
        suspect.player = player
        suspect.name = request.data["name"]
        suspect.description = request.data["description"]
        guilty = Guilty.objects.get(pk=request.data["guiltyId"])
        suspect.guilty = guilty
        movie = Movie.objects.get(pk=request.data["movieId"])
        suspect.suspect_image_url = request.data["suspectImageUrl"]
        suspect.movie = movie
       
        suspect.save()


        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single suspect
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            suspect = Suspect.objects.get(pk=pk)
            suspect.delete()

            return Response({}, status=status.HTTP_204_NO_NAME)

        except Suspect.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to suspects resource
        Returns:
            Response -- JSON serialized list of suspects
        """
        suspects = Suspect.objects.all()
        player = self.request.query_params.get('type', None)
        if player is not None:
            suspects = suspects.filter(player__id=player)

        guilty = self.request.query_params.get('type', None)
        if guilty is not None:
            suspects = suspects.filter(guilty__id=guilty)
        
        movie = self.request.query_params.get('type', None)
        if movie is not None:
            suspects = suspects.filter(movie__id=movie)


        serializer = SuspectSerializer(
            suspects, many=True, context={'request': request})
        return Response(serializer.data)

class SuspectSerializer(serializers.ModelSerializer):
    """JSON serializer for suspects
    Arguments:
        serializer type
    """
    class Meta:
        model = Suspect
        fields = ('id', 'name', 'description', 'guilty', 'movie',  'suspect_image_url')
        depth = 2
