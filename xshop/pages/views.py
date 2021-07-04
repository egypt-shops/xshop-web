from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from xshop.shops.models import Shop


class Home(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.GET.get("action") == 'search':
            search_by = request.GET.get("search_by")
            shops = Shop.objects.filter(name__icontains=search_by)
            context = {
                "shops": shops,
            }
            
        else:
            context = {
                "shops": Shop.objects.all(),
            }
        return render(self.request, "pages/home.html", context)

    template_name = "pages/home.html"
