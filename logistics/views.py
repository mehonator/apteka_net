from django.shortcuts import render
from django.views.generic import DetailView, ListView

from logistics.models import Delevery


def index(request):
    return render(request, "logistics/index.html")


class DeleveryList(ListView):
    model = Delevery
    context_object_name = "deleveries"
    template_name = "logistics/deleveris.html"


class DeleveryDetail(DetailView):
    model = Delevery
    context_object_name = "delevery"
    template_name = "logistics/delevery_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = self.object.products.all()
        return context
