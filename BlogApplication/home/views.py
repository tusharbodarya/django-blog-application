from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from django.core.paginator import Paginator

class PublicBlogView(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = Blog.objects.filter(Q(title=search) | Q(blog_text=search))
            page_number=request.GET.get('page',1)
            paginator = Paginator(blogs,1)
            serializer = BlogSerializer(paginator.page(page_number), many=True)
            
            
            return Response({
                'status': True,
                'message': 'Blog List.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = Blog.objects.filter(Q(title=search) | Q(blog_text=search))

            serializer = BlogSerializer(blogs, many=True)
            return Response({
                'status': True,
                'message': 'Blog List.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'somthing went wrong',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'status': True,
                'message': 'Blog is created.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        try:
            data = request.data
            
            blog = Blog.objects.filter(uid = data.get('uid'))
            if not blog.exists():
                return Response({
                    'status': False,
                    'message': 'Blog not found.'
                }, status=status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response({
                    'status': False,
                    'message': 'You can not update this blog.'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            serializer = BlogSerializer(blog[0], data=data, partial=True)
            
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'somthing went wrong',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'status': True,
                'message': 'Blog is Updated.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self,request):
        try:
            data = request.data
            
            blog = Blog.objects.filter(uid = data.get('uid'))
            if not blog.exists():
                return Response({
                    'status': False,
                    'message': 'Blog not found.'
                }, status=status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response({
                    'status': False,
                    'message': 'You can not delete this blog.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()
            return Response({
                'status': True,
                'message': 'Blog is Deleted.',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': False,
                'message': 'Something went wrong.',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)