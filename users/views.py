from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer, ChildSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from django.http import JsonResponse


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        print(user)
        serializer = RegisterSerializer(user)

        return response.Response({'user':serializer.data})


class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self,request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class RegisterAPIView(GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return render(request, 'registration_success.html')  # Render a success page
#         else:
#             return render(request, 'registration_failure.html', {'errors': serializer.errors})
    
class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        user = authenticate(username = email, password = password)


        if user:
            serializer = self.serializer_class(user)

            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response({'message':'Invalid Credentials, try again'}, status=status.HTTP_401_UNAUTHORIZED)
    

class ChildRegistrationAPIView(GenericAPIView):
    serializer_class = ChildSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            child = serializer.save()
            return response.Response({'message': 'Child registered successfully', 'child_id': child.id}, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

