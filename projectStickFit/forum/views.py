from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View

from projectStickFit.forum.forms import CommentForm, ForumPostForm
from projectStickFit.forum.models import ForumPost, Like


# Create your views here.

class ForumPostListView(ListView):
    model = ForumPost
    template_name = "forum/forum_list.html"
    context_object_name = "posts"
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_posts = {post.pk: post.likes.filter(user=self.request.user).exists() for post in context['posts']}
        context['liked_posts'] = liked_posts
        return context


class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = "forum/forum_post_detail.html"
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all()
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        context['comments'] = comments
        liked = self.object.likes.filter(user=self.request.user).exists()
        context['liked'] = liked
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('forum_post_detail', pk=post.pk)
        return self.render_to_response(self.get_context_data(comment_form=comment_form))


class ForumPostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'forum/create_forum_post.html'
    success_url = reverse_lazy('forum_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Like a Post (Custom View)
class LikePostView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        post = ForumPost.objects.get(pk=kwargs['pk'])
        source = self.request.POST.get('source', None) or self.request.GET.get('source', None)
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.get(post=post, user=request.user).delete()  # Remove like
        else:
            Like.objects.create(post=post, user=request.user)  # Add like
        if source == 'post-detail':
            return redirect('forum_post_detail', pk=post.id)
        else:
            return redirect('forum_list')
