from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Category,Vehicle,Profile,Rental
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from .forms import ContactForm,RentalForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


import logging



# Create your views here.


def home(request):
    
    categories=Category.objects.all()
    vehicles=Vehicle.objects.all()
    
    return render(request,'home.html',{'categories':categories,'vehicles':vehicles})

def detail(request,vehicle_type):
    categories=Category.objects.all()
    vehicles=Vehicle.objects.filter(type=vehicle_type)
    
    return render(request,'detail.html',{'categories':categories,'vehicles':vehicles})


def search(request):
    query = request.GET.get('q', '').strip()
    location = request.GET.get('location', '').strip()  # Get location parameter

    categories = Category.objects.all()
    vehicles = Vehicle.objects.none()

    if query:
        vehicles = Vehicle.objects.filter(
            Q(title__icontains=query) |
            Q(type__icontains=query)
        )
        
       

    return render(request, 'search.html', {
        'vehicles': vehicles,
        'query': query,
        'location': location,
        'categories': categories
    })



def logout_view(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('vehicles:home')





def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        logger = logging.getLogger(__name__)
        if form.is_valid():
            logger.debug(f'''Contact Details{form.cleaned_data['name']}
                         {form.cleaned_data['email']}
                         {form.cleaned_data['message']}'''
                )
            success_message='Your Email has been sent!'
            return render(request, "contact.html",{'form':form,'success_message':success_message})
        else:
            logger.debug("Form validation become error")
    
        return render(request, "contact.html",{'form':form,'name':name,'email':email,'message':message})
    return render(request, "contact.html")



def rules_regulation(request):
    return render(request,'rules_regulation.html')



def rental_form(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    categories = Category.objects.all()

    if request.method == "POST":
        pickup_raw = request.POST.get("pickup_time")
        return_raw = request.POST.get("return_time")
        delivery_address = request.POST.get("delivery_address")

        if not pickup_raw or not return_raw or not delivery_address: 
            messages.error(request, "Please fill all fields")
            return redirect(request.path)

        pickup_time = timezone.make_aware(datetime.fromisoformat(pickup_raw))
        return_time = timezone.make_aware(datetime.fromisoformat(return_raw))
        
        # ADD THIS: Check if pickup time is in the past
        if pickup_time < timezone.now():
            messages.error(
                request,
                "Pickup date & time cannot be in the past."
            )
            return redirect(request.path)
        
        if return_time <= pickup_time:
            messages.error(
                request,
                "Return date & time must be after pickup date & time."
            )
            return redirect(request.path)

        Rental.objects.create(
            user=request.user,
            vehicle=vehicle,
            pickup_time=pickup_time,
            return_time=return_time,
            delivery_address=delivery_address,
            status="pending"
        )

        messages.success(request, "🎉 Vehicle rented successfully!")
        return redirect("vehicles:success")
    
    return render(request, "rental.html", {
        "vehicle": vehicle,
        "categories": categories
    })


@login_required(login_url='vehicles:login')
def rules(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, 'rules.html', {'vehicle': vehicle})







def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        mobile = request.POST.get("mobile", "").strip()

        if not all([username, email, password, mobile]):
            messages.error(request, "All fields are required!")
            return redirect("vehicles:signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("vehicles:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("vehicles:signup")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                Profile.objects.get_or_create(
                    user=user,
                    defaults={"mobile": mobile}
                )

            messages.success(request, "Signup successful! Please login.")
            return redirect("vehicles:login")

        except IntegrityError:
            messages.error(request, "Signup failed due to duplicate data.")
            return redirect("vehicles:signup")

    return render(request, "signup.html")


def login_view(request):
    print("LOGIN VIEW HIT", request.method)
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please enter both username and password!")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password!")
            return render(request, "login.html")

        auth_login(request, user)
        messages.success(request, "Login successful!")
        return redirect("vehicles:home")

    return render(request, "login.html")



def success_page(request):
    return render(request,'success.html')

def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user).select_related("vehicle").order_by("-pickup_time")
    
    # Update status for each rental based on current time
    for rental in rentals:
        rental.update_status()

    return render(request, "my_rentals.html", {
        "rentals": rentals
    })
    
def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, 'vehicle_detail.html', {'vehicle': vehicle})


@login_required
@require_POST
def cancel_rental(request, rental_id):
    try:
        rental = Rental.objects.get(id=rental_id, user=request.user)
        
        # Prevent cancellation if already cancelled or completed
        if rental.status == 'cancelled':
            return JsonResponse({'success': False, 'error': 'Already cancelled'})
        
        if rental.status == 'completed':
            return JsonResponse({'success': False, 'error': 'Cannot cancel completed rental'})
        
        # Cancel the rental
        rental.status = 'cancelled'
        rental.save()
        return JsonResponse({'success': True})
        
    except Rental.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Rental not found'})



    
    
