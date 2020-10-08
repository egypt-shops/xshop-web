from django.shortcuts import render
from django.views.generic import View, TemplateView


class Home(View):
    def get(self, request):
        return render(request, "pages/home.html")


class SwaggerApi(TemplateView):
    extra_context = {"schema_url": "schema"}
    template_name = "pages/swagger-ui.html"
