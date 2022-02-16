from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, UserSerializerWithToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'why is the sky blue?  why is water wet?'

    #     return token

    # commented out function above puts the username and a message encrypted into the access token
    # below function serializes data and makes it accessible in the API, making it easier to grab from the frontend

    def validate(self, attrs):
        data = super().validate(attrs)
        # data['username'] = self.user.username
        # data['email'] = self.user.email

        # changing to for loop to output the data from the serializer instead of adding manually
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
