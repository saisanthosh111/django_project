from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from myapp.models import Contact
# from example.config import pagination
posts = [
{
    'author':'CoreyMs',
    'title':'blog post1',
    'content':'first post content',
    'date_posted':'august 27,2018'
},
{
    'author':'john doe',
    'title':'blog post 2',
    'content':'second post content',
    'date_posted':'august 28,2018'
}
]
def home(request):
         context = {
              #'posts' : posts
              'posts' :Post.objects.all()
         }
         return render(request, 'blog/home.html', context)

class PostListView(ListView):
     model = Post
     template_name = 'blog/home.html'
     #default it will look for list but now we changed
     #the object to posts and ask it to loop over it
     #by using this we will have an ordering in it
     context_object_name = 'posts'
     ordering = ['-date_posted']
     paginate_by = 4
     #if we remove - then oldest one is at the top
class UserPostListView(ListView):
     model = Post
     template_name = 'blog/user_posts.html'
     context_object_name = 'posts'
     paginate_by = 4

     def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        # comments = comment.object.filter(post=post).order_by('-date_posted')
        return Post.objects.filter(author=user).order_by('-date_posted')
class PostDetailView(DetailView):
     model = Post
     template_name='blog/post_detail.html'
     def get_context_data(self,*args,**kwargs):
         context = super(PostDetailView,self).get_context_data(**kwargs)
         stuff = get_object_or_404(Post,id=self.kwargs['pk'])
         comments = Comment.objects.filter(post=stuff,reply=None ).order_by('-id')
         total_likes = stuff.total_likes()
         liked = False
         if stuff.likes.filter(id=self.request.user.id).exists():
             liked = True
         comment_form = CommentForm()
         context["total_likes"]=total_likes
         context["liked"]=liked
         context["comments"]=comments
         context["comment_form"]=comment_form
         return context
     def post(self, request, pk):
       post = get_object_or_404(Post, pk=pk)
       form = CommentForm(request.POST)

       if form.is_valid():
           content = request.POST.get('content')
           reply_id = request.POST.get('comment_id')
           comment_qs = None
           if reply_id:
               comment_qs = Comment.objects.get(id=reply_id)
           comment = Comment.objects.create(post=post,user=request.user,content=content,reply=comment_qs)
           comment.save()
           return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))
     # def get_queryset(self):
     #    # the_post_obj = Post.objects.get(self.pk==Post.pk)
     #    comment_objs = Comment.objects.filter(post=Post.pk)
     #    # mydict = {'the_post':the_post_obj}
     #    # return mydict
     #    template_name="blog/post_detail.html"

class PostCreateView(LoginRequiredMixin,CreateView):
     model = Post
     fields = ['title','content','city']


     def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
     model = Post
     fields = ['title','content','city']


     def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


     def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url='/home/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def LikeView(request,pk):
    post=get_object_or_404(Post,pk=pk)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))

# def comment_view(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST or None)
#         if comment_form.is_valid():
#             content = request.POST.get('content')
#             comment = Comment.objects.create(post=post,user=request.user,content=content)
#             comment.save()
#     else:
#         comment_form = CommentForm()
    return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))
def about(request):
    return render(request, 'blog/about.html',{'title': 'about'})
def home1(request):
    return render(request, 'blog/instant.html')
def home2(request):
    return render(request,'blog/faq.html',{'title':'faq'})
# def post_detail(request,comment_id):
    # post = get_object_or_404(Post)z
    # comments = Comment.objects.filter(post=post).order_by('-comment_id')
    # context = {
    #  'post':post,
    #  'comments':comments,
    #  }
    # return render(request, 'blog/post_detail.html')


# def search(request):
#     template_name="blog/post_list.html"
#     query = request.GET.get('q')
#     # results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
def search(request):
    query = request.GET.get('query',"")
    if len(query)>78:
        allposts=Post.objects.none()
    else:
        allpostsTitle = Post.objects.filter(title__icontains=query)
        allpostsContent = Post.objects.filter(content__icontains=query)
        allposts = allpostsTitle.union(allpostsContent)
    if allposts.count() == 0:
        messages.warning(request,f'No search results found please refine your query')

    paginator = Paginator(allposts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params = {'query':query,'page_obj': page_obj}
    return render(request,'blog/search.html',params)
