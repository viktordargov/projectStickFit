from django.views.generic import TemplateView
from django.shortcuts import render


# Create your views here.

class HomePage(TemplateView):
    template_name = 'common/home-page.html'


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)
