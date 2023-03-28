from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView

from flights.forms import FlightModelForm, FlightSearchForm
from flights.models import Flight
from flights.utils import search_and_filter_tickets


@login_required
def search_page(request):
    form = FlightSearchForm()
    return render(request, 'flights/search_page.html', {'form': form})


@login_required
def search_flight(request):
    if request.method == 'POST':
        form = FlightSearchForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            try:
                # make search
                context = search_and_filter_tickets(request, form)
                tickets_from_search = list(context.get('tickets'))
                lst = Paginator(tickets_from_search, 100)

                page_number = request.GET.get('page')
                page_obj = lst.get_page(page_number)

                context['page_obj'] = page_obj
                data = form.cleaned_data
                context['countries'] = {"from": data['from_country'], "to": data['to_country']}

            except ValueError as e:
                messages.error(request, e)
                context = {'form': form}

        else:
            messages.error(request, 'No data entered for the search!')
    else:
        messages.error(request, 'No data entered for the search!')
        form = FlightSearchForm()
        context = {'form': form}

    return render(request, 'flights/search_page.html', context)


@login_required
def add_flight(request):

    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            id = data['id']
            price = data['price']
            travel_time = data['travel_time']
            availability = data['availability']
            local_departure = data['local_departure']
            deep_link = data['deep_link']
            from_country = data['from_country']
            to_country = data['to_country']
            from_city = data['from_city']
            to_city = data['to_city']
            from_airport = data['from_airport']
            to_airport = data['to_airport']
            user_id = data['user_id']
            name = f"Flight to {to_city}"

            fields = ['name', 'id', 'price', 'travel_time', 'availability', 'local_departure', 'deep_link',
                      'from_country', 'to_country', 'to_city', 'from_city', 'from_airport', 'to_airport', 'user_id'
                      ]

            form = FlightModelForm(
                initial={
                    'name': name,
                    'id': id,
                    'price': price,
                    'travel_time': travel_time,
                    'local_departure': local_departure,
                    'deep_link': deep_link,
                    'from_country': from_country,
                    'to_country': to_country,
                    'to_city': to_city,
                    'from_city': from_city,
                    'from_airport': from_airport,
                    'to_airport': to_airport,
                    'user_id': user_id,
                    'availability': availability,
                }
            )
            context['form'] = form

        return render(request, 'flights/create.html', context)
    else:
        messages.error(request, "Can't add ticket that does not exist!")
        return redirect('/flights')


@login_required
def save_flight(request):

    if request.method == 'POST':
        form = FlightModelForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket added successfully!')
            return redirect('/flights')

        else:
            messages.error(request, "Can't add ticket that does not exist!")
            return render(request, 'flights/create.html', {'form': form})
    else:
        messages.error(request, "Can't add ticket that does not exist!")
        return redirect('/flights')


@login_required
def flight_list(request):
    user_tickets = Flight.objects.filter(user_id=request.user.id)
    lst = Paginator(user_tickets, 10)
    context = {'tickets': user_tickets}

    page_number = request.GET.get('page')
    page_obj = lst.get_page(page_number)

    context['page_obj'] = page_obj
    context['space_count'] = [0 for _ in range(11 - len(context['page_obj']))]

    return render(request, 'flights/list.html', context)


class FlightDetailView(DetailView):
    queryset = Flight.objects.all()
    template_name = 'flights/detail.html'


class FlightDeleteView(SuccessMessageMixin, DeleteView):
    model = Flight
    template_name = "flights/delete.html"
    success_url = reverse_lazy('flights:flight_list')
    success_message = "Ticket deleted successfully!"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
