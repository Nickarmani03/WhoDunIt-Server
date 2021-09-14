from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Suspect

class SuspectView(ViewSet):
    """WHODUNIT Suspects"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized suspect instance
        """

        # Uses the token passed in the `Authorization` header
        
        suspect = Suspect()
        suspect.name = request.data["name"]
        suspect.is_guilty = request.data["isGuilty"]
        suspect.description = request.data["description"]
        
        

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
        
        suspect = Suspect()
        suspect.name = request.data["name"]        
        suspect.is_guilty = request.data["isGuilty"]
        suspect.description = request.data["description"]
        # suspect.movie = request.data["movie"]
        

        # movie = Movie.objects.get(pk=request.data["movieId"])
        # suspect.movie = movie
        suspect.save()


        return Response({}, status=status.HTTP_204_NO_NAME)

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


        # movie = self.request.query_params.get('movie', None)  # <<not sure about 'movie' here
        # if movie is not None:
        #     suspect = suspect.filter(movie__id=movie)

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
        fields = ('id', 'name', 'is_guilty')
        # depth = 1
