from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from whodunitapi.models import Player


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a player
    Method arguments:
      request -- The full HTTP request object
    '''

    # Use the built-in authenticate method to verify
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)
    data = {}

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)

    else:
        data = {'valid': False}
        return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new player for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    # Now save the extra info in the whodunitapi_player table
    player = Player.objects.create(
        user=new_user,
        bio=request.data['bio'],
        profile_image_url=request.data['profile_image_url']
    )

    # Commit the user to the database by saving it
    player.save()

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token to the client
    data = {
        'token': token.key
    }
    return Response(data, status=status.HTTP_201_CREATED)
