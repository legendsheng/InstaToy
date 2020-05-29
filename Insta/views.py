from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from annoying.decorators import ajax_request
from Insta.models import Post, Like, UserConnection, InstaUser, Comment

from django.contrib.auth.forms import UserCreationForm
from Insta.form import CustomUserCreationForm, CustomPostCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class HelloWorld(TemplateView):
    template_name = 'test.html'

class PostsView(ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return 

        current_user = self.request.user
        following = set()
        for conn in UserConnection.objects.filter(follows_user=current_user).select_related('followed_user'):
            following.add(conn.followed_user)
        return Post.objects.filter(author__in=following)

class FollowersView(ListView):
    model = InstaUser
    template_name = 'followers.html'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return 

        current_user = self.kwargs['pk']
        following = set()
        for conn in UserConnection.objects.filter(followed_user=current_user).select_related('follows_user'):
            following.add(conn.follows_user)
        return InstaUser.objects.filter(username__in=following)

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        liked = Like.objects.filter(post=self.kwargs.get('pk'), user=self.request.user).first()
        if liked:
            data['liked'] = 1
        else:
            data['liked'] = 0
        return data

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomPostCreationForm
    template_name = 'post_create.html'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['title']

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy("posts")
    login_url = 'login'

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')[:20]


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("login")

class UserDetailView(DetailView):
    model = InstaUser
    template_name = 'user_detail.html'

class EditUserView(LoginRequiredMixin,UpdateView):
    model = InstaUser
    template_name = 'user_update.html'
    fields = ['profile_pic', 'username']
    login_url = 'login'
    def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          userid=self.kwargs['pk']
          return reverse_lazy('user_detail', kwargs={'pk': userid})

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

@ajax_request
def toggleFollow(request):
    current_user = InstaUser.objects.get(pk=request.user.pk)
    follow_user_pk = request.POST.get('follow_user_pk')
    follow_user = InstaUser.objects.get(pk=follow_user_pk)

    try:
        if current_user != follow_user:
            if request.POST.get('type') == 'follow':
                connection = UserConnection(follows_user=current_user, followed_user=follow_user)
                connection.save()
            elif request.POST.get('type') == 'unfollow':
                UserConnection.objects.filter(follows_user=current_user, followed_user=follow_user).delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'type': request.POST.get('type'),
        'follow_user_pk': follow_user_pk
    }

@ajax_request
def addComment(request):
    comment_text = request.POST.get('comment_text')
    post_pk = request.POST.get('post_pk')
    post = Post.objects.get(pk=post_pk)
    commenter_info = {}

    try:
        comment = Comment(comment=comment_text, user=request.user, post=post)
        comment.save()

        username = request.user.username

        commenter_info = {
            'username': username,
            'comment_text': comment_text
        }

        result = 1
    except Exception as e:
        print(e)
        result = 0

    return {
        'result': result,
        'post_pk': post_pk,
        'commenter_info': commenter_info
    }