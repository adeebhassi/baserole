from django.shortcuts import render,redirect
from .forms import RoleSelectionForm
# Create your views here.
# accounts/views.py
from django.shortcuts import render, get_object_or_404
from .models import Patient, Doctor, Medicine,User,Role
from .middleware import role_permission
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home_view(request):
    return render(request,'home.html')

@role_permission(["doctor"])
def doctor_dashboard(request):
    patients = Patient.objects.all()
    nurses = User.objects.filter(roles__name="Nurse")
    return render(request, "doctor_dashboard.html", {"patients": patients, "nurses": nurses})

@role_permission(["nurse"])
def nurse_dashboard(request):
    doctors = User.objects.filter(roles__name="Doctor")
    patients = Patient.objects.all()
    return render(request, "nurse_dashboard.html", {"doctors": doctors, "patients": patients})

@role_permission(["patient"])
def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, "patient_dashboard.html", {"patient": patient})

@role_permission(["pharmacist"])
def pharmacist_dashboard(request):
    patients = Patient.objects.all()
    medicines = Medicine.objects.all()
    return render(request, "pharmacist_dashboard.html", {"patients": patients, "medicines": medicines})


def role_selection_view(request):
    if request.method == "POST":
        form = RoleSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            # Set the selected role as active_role
            request.user.active_role = form.cleaned_data["role"]
            request.user.save()

            # Redirect to the dashboard based on the selected role
            role_name = request.user.active_role.name.lower()
            if role_name == "doctor":
                return redirect("doctor_dashboard")
            elif role_name == "nurse":
                return redirect("nurse_dashboard")
            elif role_name == "patient":
                return redirect("patient_dashboard")
            elif role_name == "pharmacist":
                return redirect("pharmacist_dashboard")
            else:
                return redirect("home")  # Fallback in case of an unknown role
    else:
        form = RoleSelectionForm(user=request.user)
    return render(request, "role_selection.html", {"form": form})


def signup_view(request):
    if request.method == 'POST':
        # Make sure the field names match exactly with the form input names
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            try:
                # Create user using the custom user model
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Account created successfully!")
                  # Log the user in after signup
                return redirect('login')  # Redirect to home page
            except Exception as e:
                messages.error(request, f"Error: {e}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        selected_role_id = request.POST.get("role")  # Get the selected role from the form

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the selected role is valid for this user
            if selected_role_id and user.roles.filter(id=selected_role_id).exists():
                selected_role = Role.objects.get(id=selected_role_id)
                print(selected_role)
                user.active_role = str(selected_role)  # Set the selected role as the active role
                user.save()

                login(request, user)
                messages.success(request, f"You have logged in as {selected_role.name}.")
                
                # Redirect to the role-specific dashboard
                if selected_role.name.lower() == "doctor":
                    return redirect("doctor_dashboard")
                elif selected_role.name.lower() == "nurse":
                    return redirect("nurse_dashboard")
                elif selected_role.name.lower() == "patient":
                    return redirect("patient_dashboard")
                elif selected_role.name.lower() == "pharmacist":
                    return redirect("pharmacist_dashboard")
                else:
                    return redirect("home")
            else:
                messages.error(request, "Invalid role selected.")
        else:
            messages.error(request, "Invalid username or password.")
        return redirect("login")
    roles=Role.objects.all()
    print("rolse",roles)
    context={
        'roles':roles
    }

    return render(request, "login.html",context)
def logout_view(request):
    user=request.user
    user.active_role=''
    user.save()
    print('rols',user.active_role)
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to the login page after logging out


def welcome_view(request):
    return render(request,'welcome.html')
