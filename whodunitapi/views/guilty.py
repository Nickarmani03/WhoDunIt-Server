"""View module for handling requests about guiltys"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from whodunitapi.models import Guilty


class GuiltyView(ViewSet):
    """WHODUNIT guilty"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single guilty
        Returns:
            Response -- JSON serialized guilty
        """
        try:
            guilty = Guilty.objects.get(pk=pk)
            serializer = GuiltySerializer(guilty, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all guilty
        Returns:
            Response -- JSON serialized list of guilty
        """
        guiltys = Guilty.objects.all()

        # Note the additional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GuiltySerializer(
            guiltys, many=True, context={'request': request})
        return Response(serializer.data)

class GuiltySerializer(serializers.ModelSerializer):
    """JSON serializer for guilty
    Arguments:
        serializers
    """
    class Meta:
        model = Guilty
        fields = ('id', 'label')
