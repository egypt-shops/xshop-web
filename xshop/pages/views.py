from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from xshop.shops.models import Shop


class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {
            "shops": Shop.objects.all(),
        }
        return render(self.request, "pages/home.html", context)

    template_name = "pages/home.html"
