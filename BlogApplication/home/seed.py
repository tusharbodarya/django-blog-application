from faker import Faker
fake=Faker()
import random
from django.contrib.auth.models import User
from home.models import Blog
from django.core.files.uploadedfile import SimpleUploadedFile
def db_seed(n=10)->None:
    try:
        for _ in range(n):
            user_obj = User.objects.all()
            random_index = random.randint(0,len(user_obj)-1)
            user = user_obj[random_index]
            title = fake.name()
            blog_text = fake.text()
            main_image = SimpleUploadedFile(name='test_image.jpg', content=open('./blogs/1.jpg', 'rb').read(), content_type='image/jpeg')
            
            blog_obj = Blog.objects.create(
                user=user,
                title=title,
                blog_text=blog_text,
                main_image=main_image
            )
    except Exception as e:
        print(e)