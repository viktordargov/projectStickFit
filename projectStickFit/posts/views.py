from django.shortcuts import render, redirect
from .models import Posts
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'posts/posts_list.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts_list')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})
