from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "pages/home.html"
class LandingPage(TemplateView):
	template_name = "pages/landingpage.html"
