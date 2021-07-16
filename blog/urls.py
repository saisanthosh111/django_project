from django.urls import path
from .views import PostListView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,PostDetailView,LikeView,search
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    # path('',views.PostListView.as_view(template_name='blog/home.html'),name='blog-home'),
    # path('',views.home1,name='blog-instant'),
    path('faq',views.home2,name='faq'),
    # path('/home/', PostListView.as_view(),name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(),name = 'user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(),name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(),name = 'post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name = 'post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name = 'post-delete'),
    path('about/', views.about,name = 'blog-about'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('search',views.search,name='search'),
    # path('comment/<int:pk>',comment_view,name='comment_post'),
]
#<app>/<model>_<viewtype>.html
# #pk means primary key
# post = get_object_or_404(Post,id=id,slug=slug)
# comments = Comment.object.filter(post=post).order_by('-date_posted')
# context = {
#  'post':post,
#  'comments':comments,
#  }
# return render(request, 'blog/post_detail.html', context)
