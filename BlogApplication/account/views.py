from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer
from rest_framework import status

class RegisterView(APIView):
    
    def post(self,request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'somthing went wrong',
                    'data': serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'status':True,
                'message':'Your account is created.',
                'data': serializer.data
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                    'status':False,
                    'message':'somthing went wrong',
                    'data': str(e)
                },status=status.HTTP_400_BAD_REQUEST)
            
class LoginView(APIView):
    
    def post(self,request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'status':False,
                    'message':'somthing went wrong.',
                    'data': serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)
            return Response({
                'status':True,
                'message':'Your account is created.',
                'data': response
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                    'status':False,
                    'message':'somthing went wrong',
                    'data': str(e)
                },status=status.HTTP_400_BAD_REQUEST)