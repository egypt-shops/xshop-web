from django.views.generic import TemplateView


class SwaggerUi(TemplateView):
    extra_context = {"schema_url": "pages_api:schema"}
    template_name = "pages/swagger_ui.html"
