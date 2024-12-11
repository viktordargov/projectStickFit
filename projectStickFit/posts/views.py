from django.shortcuts import render, redirect
from .models import Posts
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from cloudinary.uploader import destroy


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


class DeleteImageView(View):
    def post(self, request, *args, **kwargs):
        # Extract image ID from the request body (JSON payload)
        try:
            import json
            data = json.loads(request.body)  # Parse JSON payload
            image_id = data.get("image_id")  # Get image ID from request body
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        if not image_id:
            return JsonResponse({"error": "No image ID provided"}, status=400)

        try:
            # Find the image in the database
            image = Posts.objects.get(pk=image_id)

            # Delete the image on Cloudinary
            response = destroy(image.image.public_id)  # Delete using the correct public ID

            if response.get("result") == "ok":
                # Remove the reference from the database
                image.delete()
                return JsonResponse({"message": "Image deleted successfully"})
            else:
                return JsonResponse({"error": "Failed to delete image from Cloudinary"}, status=400)
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Image not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
