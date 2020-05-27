from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from annoying.decorators import ajax_request
from Insta.models import Post, Like, UserConnection, InstaUser

from django.contrib.auth.forms import UserCreationForm
from Insta.form import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

    # def get_queryset(self):
    #     if not self.request.user.is_authenticated:
    #         return 

    #     current_user = self.request.user
    #     following = set()
    #     for conn in UserConnection.objects.filter(follows_user=current_user).select_related('followed_user'):
    #         following.add(conn.followed_user)
    #     return Post.objects.filter(author__in=following)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    login_url = 'login'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")
    login_url = 'login'

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'
@ajax_request
def addLike(request):
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    try:
        like = Like(post=post, user=request.user)
        like.save()
        result = 1
    except Exception as e:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        result = 0

    return {
        'result': result,
        'post_pk': post_pk
    }