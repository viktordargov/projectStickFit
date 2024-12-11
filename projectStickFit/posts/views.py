from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Posts
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from cloudinary.uploader import destroy


def post_list(request):
    posts = Posts.objects.all().order_by('-created_at')

    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/posts_list.html', {'page_obj': page_obj})


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


class DeleteImageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        try:
            import json
            data = json.loads(request.body)
            image_id = data.get("image_id")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        if not image_id:
            return JsonResponse({"error": "No image ID provided"}, status=400)

        try:

            image = Posts.objects.get(pk=image_id)

            if image.user != request.user and not request.user.is_staff:
                return JsonResponse({"error": "You do not have permission to delete this image."}, status=403)


            response = destroy(image.image.public_id)

            if response.get("result") == "ok":

                image.delete()
                return JsonResponse({"message": "Image deleted successfully"})
            else:
                return JsonResponse({"error": "Failed to delete image from Cloudinary"}, status=400)
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Image not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
