from django.views.generic import TemplateView
from django.shortcuts import render
from xshop.shops.models import Shop


class Home(TemplateView):
    def get(self, *args, **kwargs):
        shops = []
        num = Shop.objects.all().count()
        for i in range(1, num + 1):
            shops.append(Shop.objects.get(id=i))

        context = {
            "shops": shops,
        }
        return render(self.request, "pages/home.html", context)

    template_name = "pages/home.html"
