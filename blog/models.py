from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    title  = models.CharField(max_length=100)
    city = models.CharField(max_length=100,default="")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name="blog_posts")
    # comments = models.ManyToManyField(User,related_name="comment_posts")
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.title
    #in this we are just passing an argument but not executing so we have removed parenthesis

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=160)
    timestamp=models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment',null=True,related_name="replies",on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.post.title,str(self.user.username))
