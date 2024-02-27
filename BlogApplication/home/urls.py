from django.urls import path
from home.views import BlogView,PublicBlogView
urlpatterns = [
    path("blogs/", BlogView.as_view()),
    path("public/blogs/", PublicBlogView.as_view()),
]