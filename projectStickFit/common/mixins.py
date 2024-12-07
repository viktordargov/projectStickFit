from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render


class IsStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return HttpResponseNotFound(render(request, "404.html"))
        return super().dispatch(request, *args, **kwargs)
