from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Value
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, DeleteView

from projectStickFit.forum.forms import CommentForm, ForumThreadForm
from projectStickFit.forum.models import ForumThreads, Like


class ForumThreadListView(ListView):
    model = ForumThreads
    template_name = "forum/forum_list.html"
    context_object_name = "threads"
    ordering = ['-created_at']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            liked_threads = {
                thread.pk: thread.likes.filter(user=self.request.user).exists()
                for thread in context['threads']
            }
        else:
            liked_threads = {}

        context['liked_threads'] = liked_threads
        return context

    def get_queryset(self):
        queryset = ForumThreads.objects.all()
        user_query = self.request.GET.get('user_query', '')

        if user_query:
            return queryset.filter(
                Q(title__icontains=user_query) | Q(content__icontains=user_query)
            ).order_by('-created_at')
        return ForumThreads.objects.all().order_by('-created_at')


class ForumThreadDetailView(DetailView):
    model = ForumThreads
    template_name = "forum/forum_thread_detail.html"
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        comments = thread.comments.all()
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        context['comments'] = comments
        if self.request.user.is_authenticated:
            liked = self.object.likes.filter(user=self.request.user).exists()
            context['liked'] = liked
        return context

    def post(self, request, *args, **kwargs):
        thread = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            return redirect('forum_thread_detail', pk=thread.pk)
        return self.render_to_response(self.get_context_data(comment_form=comment_form))


class ForumThreadCreateView(LoginRequiredMixin, CreateView):
    model = ForumThreads
    form_class = ForumThreadForm
    template_name = 'forum/create_forum_thread.html'
    success_url = reverse_lazy('forum_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ForumThreadDeleteView(LoginRequiredMixin, DeleteView):
    model = ForumThreads
    success_url = reverse_lazy('forum_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_staff:
            raise Http404("You are not authorized to delete this thread.")

        return obj


class LikeThreadView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        thread = ForumThreads.objects.get(pk=kwargs['pk'])
        source = self.request.POST.get('source', None) or self.request.GET.get('source', None)
        if Like.objects.filter(thread=thread, user=request.user).exists():
            Like.objects.get(thread=thread, user=request.user).delete()  # Remove like
        else:
            Like.objects.create(thread=thread, user=request.user)  # Add like
        if source == 'thread-detail':
            return redirect('forum_thread_detail', pk=thread.id)
        else:
            return redirect('forum_list')
