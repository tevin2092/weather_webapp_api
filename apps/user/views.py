
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import UserProfile
from .serializer import UserProfileSerializer

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        location = request.data.get('location')
        preferred_temperature_unit = request.data.get('preferred_temperature_unit')

        if not username or not password or not email:
            return Response({'error': 'Please provide all required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        user_profile = UserProfile.objects.create(user=user, location=location, preferred_temperature_unit=preferred_temperature_unit)
        
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


class UserProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if not user_profile:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if not user_profile:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not username or not password:
#             return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)

#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         try:
#             # Get the token from the user and delete it
#             token = Token.objects.get(user=request.user)
#             token.delete()
#             return Response({"success": "Successfully logged out."}, status=status.HTTP_200_OK)
#         except Token.DoesNotExist:
#             return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)