from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator

from countries.forms import CountryForm
from countries.models import Country


__all__ = (
    'home',
    'CountryListView',
    'CountryDetailView',
    'CountryCreateView',
    'CountryDeleteView',
    'CountryUpdateView',
    'fill_country_list',
)


def home(request):
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            form.save()

    form = CountryForm
    countries_from_db = Country.objects.all()
    lst = Paginator(countries_from_db, 10)

    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)

    context = {'page_obj': page_obj, "form": form}
    return render(request, 'countries/home.html', context)



class CountryListView(ListView):
    template_name = "countries/home.html"
    form = CountryForm()
    paginate_by = 10
    model = Country

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CountryForm()
        context['form'] = form
        context['space_count'] = [0 for _ in range(11 - len(context['page_obj']))]
        return context


class CountryDetailView(DetailView):
    queryset = Country.objects.all()
    template_name = 'countries/detail.html'



class CountryCreateView(SuccessMessageMixin, CreateView):
    model = Country
    form_class = CountryForm
    template_name = "countries/create.html"
    success_url = reverse_lazy("countries:home")
    success_message = "Country added successfully!"


class CountryDeleteView(SuccessMessageMixin, DeleteView):
    model = Country
    template_name = "countries/delete.html"
    success_url = reverse_lazy('countries:home')
    success_message = "Country deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CountryUpdateView(SuccessMessageMixin, UpdateView):
    model = Country
    form_class = CountryForm
    template_name = "countries/update.html"
    success_url = reverse_lazy("countries:home")
    success_message = "Changes applied successfully!"


def fill_country_list(request):
    Country.create_from_list()
    return redirect("countries:home")