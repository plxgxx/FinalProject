from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from carH_OUR import models

# Create your views here.


def welcome_page(request):
    if request.method == 'GET':
        return render(request, 'welcome.html')
    if request.method == 'POST':
        city_list = list(models.Place.objects.all().values_list('city', flat=True))
        result_city_list = list(set(city_list))
        district_list = list(models.Place.objects.all().values_list('district', flat=True))
        result_district_list = list(set(district_list))
        cursor = connection.cursor()
        type = request.POST.get('type')
        seats = request.POST.get('seats')
        city = request.POST.get('city')
        district = request.POST.get('district')

        sql_querry = f"""SELECT carH_OUR_car.id,
                                carH_OUR_car.brand,
                                carH_OUR_car.model,
                                carH_OUR_car.seats,
                                carH_OUR_car.type,
                                carH_OUR_car.city_placement,
                                carH_OUR_car.district_placement,
                                carH_OUR_car.street_placement
                                from carH_OUR_car
                                    WHERE carH_OUR_car.type = '{type}'
                                        and carH_OUR_car.seats = '{seats}'
                                        and carH_OUR_car.city_placement = '{city}'
                                        and carH_OUR_car.district_placement = '{district}'
                                
                                """
        cursor.execute(sql_querry)
        unparsed_res = cursor.fetchall()
        result = []
        for i in unparsed_res:
            res_id = i[0]
            res_brand = i[1]
            res_model = i[2]
            res_seats = i[3]
            res_type = i[4]
            res_city = i[5]
            res_district = i[6]
            res_street = i[7]
            result_dict = {"Use this id to book your car": res_id,
                           "Car brand": res_brand,
                           "Car model": res_model,
                           "Amount of seats": res_seats,
                           "Car type": res_type,
                           "City": res_city,
                           "District": res_district,
                           "Street": res_street}
            result.append(result_dict)
            if result is not None:
                return HttpResponse(result)
            else:
                return HttpResponse('No cars found! Try different parameters')


def add_car(request):
    if request.user.has_perm('car.add_car'):
        if request.method == 'GET':
            return render(request, 'add_car.html')
        if request.method == 'POST':
            brand = request.POST.get('brand')
            model = request.POST.get('model')
            seats = request.POST.get('seats')
            car_type = request.POST.get('type')
            city = request.POST.get('city')
            district = request.POST.get('district')
            street = request.POST.get('street')

            models.cartypevalidate(car_type)

            new_car = models.Car(brand=brand, model=model, seats=seats, type=car_type,
                                 city_placement=city, district_placement=district,
                                 street_placement=street)
            new_car.save()
            return HttpResponse('Car saved!')

    else:
        return HttpResponse('No rights!')




def take_car(request):
    return HttpResponse('Ok!')


def return_car(request):
    return HttpResponse('Ok!')


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        usernm = request.POST['username']
        passwrd = request.POST['password']
        user = authenticate(username=usernm, password=passwrd)
        if user is not None:
            login(request, user)
            return HttpResponse('Successful login')
        else:
            return HttpResponse('No such registered user')


def user_registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html')
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST.get('username'),
                                        email=request.POST.get('email'),
                                        password=request.POST.get('password'),
                                        first_name=request.POST.get('first'),
                                        last_name=request.POST.get('last'))
        user.save()
        return HttpResponse('User is created')


def logout_user(request):
    logout(request)
    return redirect('/login')