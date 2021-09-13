"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Genre


class GenreView(ViewSet):
    """Level up genres"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all genres
        Returns:
            Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GenreSerializer(
            genres, many=True, context={'request': request})
        return Response(serializer.data)

class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres
    Arguments:
        serializers
    """
    class Meta:
        model = Genre
        fields = ('id', 'label')
