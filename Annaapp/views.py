from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .forms import PetListingForm
from .models import PetListing,User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout as auth_logout ,authenticate, login as auth_login
from .models import signupmodel,ContactMessage,Appointment
from datetime import datetime, timedelta
from orders.models import Order
# Create your views here.
def index(request):
    return render(request, 'index.html')

def dd(request):
    return render(request, 'dd1.html')

def cici(request):
    return render(request, 'cici.html')

def butterfly(request):
    return render(request, 'butterfly.html')

def blanc(request):
    return render(request, 'blanc.html')
def splittin(request):
    return render(request, 'splittin.html')
def cd(request):
    return render(request, 'cd1.html')

def bd(request):
    return render(request, 'bd1.html')

def dutch(request):
    return render(request, 'dutch.html')
def fd(request):
    return render(request, 'fd1.html')

def rd(request):
    return render(request, 'rd1.html')
def owl(request):
    return render(request, 'owl.html')
def saddlebred(request):
    return render(request, 'saddlebred.html')
def hd(request):
    return render(request,'hd1.html')

@login_required
def contact(request):
    return render(request, 'contact.html')

def satin(request):
    return render(request, 'satin.html')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You Have been Logged out")
    return redirect('index')

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import signupmodel  # if you're using a custom model

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if username or email already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, "Passwords don't match.")
            return redirect('signup')

        # Create Django user
        django_user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Optionally create your custom signup record
        signup_record = signupmodel(
            username=username,
            email=email,
            password=password,
            confirmpassword=confirm_password
        )
        signup_record.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

@login_required
def appointment(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons')
        
        # Basic validation
        if not all([name, email, phone, date, time, persons]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'appointment.html')
            
        try:
            # Here you would typically save to database
            # For example: Appointment.objects.create(name=name, email=email, ...)
            
            messages.success(request, "Your appointment was successfully booked!")
            return redirect('appointment')  # Redirect to clear the form
        except Exception as e:
            messages.error(request, f"There was an error with your form: {str(e)}")
    
    # If GET request or form processing failed
    return render(request, 'appointment.html')

def pets(request):
    return render(request, 'pets.html')

def hawk(request):
    return render(request, 'hawk.html')

def arabian(request):
    return render(request, 'arabian.html')
@login_required 
def booking(request):
    return render(request, 'booking.html')

@login_required
def labrador(request):

    return render(request, 'labrador.html')
def fell(request):
    return render(request, 'fell.html')

def lovebirds(request):
    return render(request, 'lovebirds.html')

def bookpet(request):
    return render(request, 'bookpet.html')

def burmila(request):
    return render(request, 'burmila.html')

def birman(request):
    return render(request, 'birman.html')


def york(request):
    return render(request, 'york.html')

def maltese(request):
    return render(request, 'maltese.html')

def shihtzu(request):
    return render(request, 'shihtzu.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('index')  # or wherever you want to send them
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')



def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')


def google_login(request):
    return render(request,"google_login.html")

@login_required
def upload_pet(request):
    if request.method == 'POST':
        form = PetListingForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user  # Assign current user
            pet.save()
            print(f"✅ Pet '{pet.name}' uploaded by {request.user.username}")  # Debug print
            return redirect('my_pets')  # or wherever you want to go
    else:
        form = PetListingForm()
        print("❌ Form is invalid:")
        print(form.errors)
    return render(request, 'upload_pet.html', {'form': form})

@login_required
def my_pets(request):
    pets = PetListing.objects.filter(user=request.user)
    print(f"Found {pets.count()} pets for user {request.user.username}")
    return render(request, 'my_pets.html', {'pets': pets})  

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def delete_pet(request, pet_id):
    pet = get_object_or_404(PetListing, id=pet_id)
    pet.delete()
    return redirect('my_pets')  # or wherever you want



from django.shortcuts import render
from .models import Pet, PetBooking

def pet_list(request):
    pets = Pet.objects.filter(available=True)
    return render(request, 'pets.html', {'pets': pets})

def booking(request):
    if request.method == 'POST':
        # Handle form submission
        pet_name = request.POST.get('pet_name')
        email = request.POST.get('email')
        pet_type = request.POST.get('pet_type')
        breed = request.POST.get('breed')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        
        # Create new booking
        booking = PetBooking(
            pet_name=pet_name,
            email=email,
            pet_type=pet_type,
            breed=breed,
            address=address,
            payment_method=payment_method
        )
        booking.save()
        
        # You might want to add a success message here
        return render(request, 'booking_success.html')
    
    return render(request, 'booking.html')

@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        

        messages.success(request, "Thank you for contacting us!")
        return redirect('contact')  # Replace with the correct URL name

    return render(request, 'contact.html')

@login_required
def appointment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        persons = request.POST.get('persons')
        
        # Save to database
        Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            persons=persons,
            user=request.user  # Make sure your model has a user field
        )

        # Save to session for receipt page
        request.session['appointment_data'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'date': date,
            'time': time,
            'persons': persons,
        }
        
        messages.success(request, 'Appointment booked successfully!')
        return redirect('receipt')  # Change this to redirect to receipt

    return render(request, 'appointment.html')

@login_required
def appointment_receipt(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, user=request.user)
    return render(request, 'appointments/appointment_receipt.html', {'appointment': appointment})

def receipt(request):
    data = request.session.get('appointment_data')
    if not data:
        return redirect('appointment')
    return render(request, 'receipt.html', {'data': data})

def my_appointments_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        appointments = Appointment.objects.filter(email=email).order_by('-date', '-time')
        return render(request, 'my_appointments.html', {'appointments': appointments, 'email': email})
    return render(request, 'my_appointments.html')


def bookpet(request):
    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        email = request.POST.get('email')
        pet_type = request.POST.get('pet_type')
        breed = request.POST.get('breed')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Estimate delivery: 5 days from now
        expected_delivery = datetime.now() + timedelta(days=5)
        expected_delivery = expected_delivery.strftime('%d %B %Y')  # Pretty format like 25 April 2025

        context = {
            'pet_name': pet_name,
            'email': email,
            'pet_type': pet_type,
            'breed': breed,
            'address': address,
            'payment_method': payment_method,
            'expected_delivery': expected_delivery,
        }

        return render(request, 'bookpet.html', context)
    
    return render(request, 'bookpet.html')

@login_required
def user_receipts(request):
    appointments = Appointment.objects.filter(user=request.user)
    pet_bookings = PetBooking.objects.filter(user=request.user)
    return render(request, 'user_receipts.html', {
        'appointments': appointments,
        'pet_bookings': pet_bookings
    })