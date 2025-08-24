from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .models import UserProfile
import random

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        student_id = request.POST['student_id']
        department = request.POST['department']
        year = request.POST['year']
        
        # New fields for OTP functionality
        phone = request.POST.get('phone', '')
        full_name = request.POST.get('full_name', '')

        # CHECK ALL UNIQUE CONSTRAINTS BEFORE CREATING USER
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'users/register.html')
            
        # Check if email already exists in User model
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'users/register.html')
            
        # Check if student_id already exists
        if UserProfile.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already registered!')
            return render(request, 'users/register.html')
        
        # Check if phone already exists
        if phone and UserProfile.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered!')
            return render(request, 'users/register.html')
            
        # Check if college_email already exists
        if UserProfile.objects.filter(college_email=email).exists():
            messages.error(request, 'College email already registered!')
            return render(request, 'users/register.html')

        # Create user but don't activate yet (for OTP verification)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False  # Will be activated after OTP verification
        user.save()
        
        # Generate OTP
        otp = f"{random.randint(100000, 999999)}"
        
        # Create UserProfile with OTP
        UserProfile.objects.create(
            user=user,
            student_id=student_id,
            college_email=email,
            department=department,
            year=year,
            phone=phone,
            full_name=full_name,
            otp=otp
        )

        # Print OTP to console (for testing)
        print(f"SMS OTP: {otp} sent to {phone}")
        
        # Store user in session for OTP verification
        request.session['pending_user'] = user.username

        messages.success(request, f'Registration initiated! OTP sent to {phone}. Please verify to complete registration.')
        return redirect('verify_otp')

    return render(request, 'users/register.html')

def verify_otp(request):
    username = request.session.get('pending_user')
    if not username:
        messages.error(request, "No pending registration found!")
        return redirect('register')
    
    try:
        user = User.objects.get(username=username)
        profile = user.userprofile
    except:
        messages.error(request, "Registration not found!")
        return redirect('register')
    
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        if otp_entered == profile.otp:
            # Verify phone and activate user
            profile.is_phone_verified = True
            profile.otp = ''
            user.is_active = True
            user.save()
            profile.save()
            
            # Send welcome email
            try:
                send_mail(
                    "Welcome to Voting Portal!",
                    f"Dear {profile.full_name or user.username},\n\nThank you for registering! You can now log in to participate in elections.\n\nLogin at: http://127.0.0.1:8000/\n\nBest regards,\nVoting Team",
                    'noreply@votingportal.com',
                    [user.email],
                    fail_silently=False,
                )
                print(f"Welcome email sent to {user.email}")
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            messages.success(request, "Phone verified! Registration complete. You can now log in.")
            del request.session['pending_user']
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, 'users/verify_otp.html', {'phone': profile.phone})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            # Check if user's phone is verified (if they have a phone number)
            try:
                profile = user.userprofile
                if profile.phone and not profile.is_phone_verified:
                    messages.error(request, 'Please verify your phone number first.')
                    return render(request, 'users/login.html')
            except UserProfile.DoesNotExist:
                pass  # Old users might not have profiles yet
            
            login(request, user)
            return redirect('dashboard')  # or 'admin_dashboard' if preferred
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
