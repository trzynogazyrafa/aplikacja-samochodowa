from django.shortcuts import render, redirect
from car.forms import CarForm, CarDetailForm, CarMainForm
from car.models import Car, CarDetail, CarMain
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from website.serializers import UserSerializer, GroupSerializer, CarSerializer


# Create your views here.
def main_view(request):
    context = {}
    template = "main.html"
    if request.method == "GET":
        car_detail_form = CarDetailForm(prefix="detail")
        car_main_form = CarMainForm(prefix="main")
        context["car_detail_form"] = car_detail_form
        context["car_main_form"] = car_main_form
        return render(request, template, context)
    elif request.method == "POST":
        cars = Car.objects.select_related("main").select_related("detail").all()
        car_detail_form = CarDetailForm(request.POST, prefix="detail")
        car_main_form = CarMainForm(request.POST, prefix="main")
        if car_detail_form.is_valid() and car_main_form.is_valid():
            make = car_main_form.cleaned_data["make"]
            if make:
                cars = cars.filter(main__make=make)

            model = car_main_form.cleaned_data["model"]
            if model:
                cars = cars.filter(main__model=model)

            color = car_detail_form.cleaned_data["color"]
            if color:
                cars = cars.filter(detail__color=color)

            seats = car_detail_form.cleaned_data["seats"]
            if seats:
                cars = cars.filter(detail__seats=seats)

            fuel = car_detail_form.cleaned_data["fuel"]
            if fuel:
                cars = cars.filter(detail__fuel=fuel)

            power_min = car_detail_form.cleaned_data["power_min"]
            power_max = car_detail_form.cleaned_data["power_max"]
            # > gt
            # >= gte
            # < lt
            # <= lte
            if power_min:
                cars = cars.filter(detail__power__gte=power_min)
            if power_max:
                cars = cars.filter(detail__power__lte=power_max)

            price_min = car_detail_form.cleaned_data["price_min"]
            price_max = car_detail_form.cleaned_data["price_max"]
            if price_min:
                cars = cars.filter(detail__price__gte=price_min)
            if price_max:
                cars = cars.filter(detail__price__lte=price_max)

            production_date_start = car_detail_form.cleaned_data["production_date_start"]
            production_date_end = car_detail_form.cleaned_data["production_date_end"]
            if production_date_start:
                cars = cars.filter(detail__production_date__gte=production_date_start)
            if production_date_end:
                cars = cars.filter(detail__production_date__lte=production_date_end)

        context["cars"] = cars
        context["car_detail_form"] = car_detail_form
        context["car_main_form"] = car_main_form
        return render(request, template, context)


def car_view(request, pk):
    template = "car.html"
    context = {}
    if request.method == "GET":
        car = Car.objects.get(id=pk)
        context["car"] = car
        return render(request, template, context)
    return redirect("main")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        power_min = self.request.query_params.get("power_min")
        if power_min :
             return qs.filter(detail__power__gte=power_min)
        return qs

class CarList(generics.ListAPIView):
    serializer_class = CarSerializer

    # def get_queryset(self):
    #     queryset = Car.objects.all()
    #     power_min = self.request.query_params.get("power_min")
    #     if power_min is not None:
    #         queryset = queryset.filter(detail__power__gte=power_min)
    #     return queryset
