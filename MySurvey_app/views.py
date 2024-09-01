from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import bcrypt
import logging
from .models import User  # Ensure this matches the model definition in models.py

logger = logging.getLogger(__name__)

def log_and_reg(request):
    return render(request, 'log_and_reg.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if errors:
            for val in errors.values():
                messages.error(request, val)
            return redirect('/')
        else:
            password = request.POST['password']
            # Hash password for your security
            hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=hash_pw  # Consider using a hashed password
            )
            auth_login(request, user)  # Automatically log in the user
            messages.success(request, "Successfully registered and logged in.")
            return redirect('/index')
    return redirect('/')

def login(request):
    """Handles user login"""
    if request.method == 'POST':
        users = User.objects.filter(email=request.POST['email'])
        if users:
            logged_user = users[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                messages.success(request, "Successfully logged in.")
                return redirect('/index')  # Redirect to index.html where user can add a book
            else:
                messages.error(request, "Invalid Email/Password Combo.")
        else:
            messages.error(request, "Account not found with that email.")
    return redirect('/')

def logout(request):
    auth_logout(request)
    return redirect('/')

def index(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['userid']),
    }
    return render(request, 'index.html', context)

def process(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        colors = request.POST.getlist('color')
        plants = request.POST.getlist('plant')

        request.session['name'] = name
        request.session['color'] = colors
        request.session['plant'] = plants
        
        return redirect('result')
    return redirect('index')

def result(request):
    return render(request, 'result.html')
