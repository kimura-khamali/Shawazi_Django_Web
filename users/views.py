# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .forms import UserRegistrationForm
from .models import User
import random
import requests

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_sms(phone_number, otp):
    url = 'https://api.smsleopard.com/v1/sms/send'
    params = {
        'api_key': settings.SMSLEOPARD_API_KEY,
        'api_secret': settings.SMSLEOPARD_API_SECRET,
        'to': phone_number,
        'from': settings.SMSLEOPARD_SENDER_NAME,
        'message': f'Your OTP is: {otp}. It will expire in 10 minutes.'
    }
    
    try:
        response = requests.post(url, data=params)
        return response.status_code == 200
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        return False

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User won't be able to log in until OTP is verified
            user.save()
            
            # Generate and save OTP
            otp = generate_otp()
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()
            
            # Send OTP via SMS
            if send_otp_sms(user.phone_number, otp):
                request.session['user_id'] = user.id
                messages.success(request, 'Registration successful. Please check your phone for the OTP.')
                return redirect('verify_otp')
            else:
                user.delete()  # Delete the user if SMS sending fails
                messages.error(request, 'Failed to send OTP. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Invalid session. Please register again.')
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found. Please register again.')
        return redirect('register')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if not otp:
            messages.error(request, 'Please enter the OTP.')
        elif user.otp != otp:
            messages.error(request, 'Invalid OTP. Please try again.')
        elif not user.is_otp_valid():
            messages.error(request, 'OTP has expired. Please request a new one.')
        else:
            user.is_active = True
            user.otp = None
            user.otp_created_at = None
            user.save()
            login(request, user)
            messages.success(request, 'OTP verified successfully. You are now logged in.')
            return redirect('home')  # Redirect to home page or dashboard
    
    return render(request, 'users/verify_otp.html')

def resend_otp(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Invalid session. Please register again.')
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found. Please register again.')
        return redirect('register')
    
    otp = generate_otp()
    user.otp = otp
    user.otp_created_at = timezone.now()
    user.save()
    
    if send_otp_sms(user.phone_number, otp):
        messages.success(request, 'A new OTP has been sent to your phone.')
    else:
        messages.error(request, 'Failed to send new OTP. Please try again.')
    
    return redirect('verify_otp')
















# # users/views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib import messages
# from django.utils import timezone
# from django.conf import settings
# from .forms import UserRegistrationForm
# from .models import User
# import random

# # Import your SMS service here
# # from your_sms_service import send_sms

# def generate_otp():
#     return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# def send_otp_sms(phone_number, otp):
#     message = f'Your OTP is: {otp}. It will expire in 10 minutes.'
    
#     try:
#         # Replace this with your actual SMS sending code
#         # send_sms(phone_number, message)
#         print(f"Sending SMS to {phone_number}: {message}")  # For testing purposes
#         return True
#     except Exception as e:
#         print(f"Failed to send SMS: {str(e)}")
#         return False

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # User won't be able to log in until OTP is verified
#             user.save()
            
#             # Generate and save OTP
#             otp = generate_otp()
#             user.otp = otp
#             user.otp_created_at = timezone.now()
#             user.save()
            
#             # Send OTP via SMS
#             if send_otp_sms(user.phone_number, otp):
#                 request.session['user_id'] = user.id
#                 messages.success(request, 'Registration successful. Please check your phone for the OTP.')
#                 return redirect('verify_otp')
#             else:
#                 user.delete()  # Delete the user if SMS sending fails
#                 messages.error(request, 'Failed to send OTP. Please try again.')
#         else:
#             messages.error(request, 'Invalid form submission. Please correct the errors.')
#     else:
#         form = UserRegistrationForm()
    
#     return render(request, 'users/register.html', {'form': form})

# def verify_otp(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, 'Invalid session. Please register again.')
#         return redirect('register')
    
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         messages.error(request, 'User not found. Please register again.')
#         return redirect('register')
    
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         if not otp:
#             messages.error(request, 'Please enter the OTP.')
#         elif user.otp != otp:
#             messages.error(request, 'Invalid OTP. Please try again.')
#         elif not user.is_otp_valid():
#             messages.error(request, 'OTP has expired. Please request a new one.')
#         else:
#             user.is_active = True
#             user.otp = None
#             user.otp_created_at = None
#             user.save()
#             login(request, user)
#             messages.success(request, 'OTP verified successfully. You are now logged in.')
#             return redirect('home')  # Redirect to home page or dashboard
    
#     return render(request, 'users/verify_otp.html')

# def resend_otp(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, 'Invalid session. Please register again.')
#         return redirect('register')
    
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         messages.error(request, 'User not found. Please register again.')
#         return redirect('register')
    
#     otp = generate_otp()
#     user.otp = otp
#     user.otp_created_at = timezone.now()
#     user.save()
    
#     if send_otp_sms(user.phone_number, otp):
#         messages.success(request, 'A new OTP has been sent to your phone.')
#     else:
#         messages.error(request, 'Failed to send new OTP. Please try again.')
    
#     return redirect('verify_otp')


# # users/views.py

# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib import messages
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings
# from .forms import UserRegistrationForm
# from .models import User
# import random

# def generate_otp():
#     return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# def send_otp_email(email, otp):
#     subject = 'Your OTP for Registration'
#     message = f'Your OTP is: {otp}. It will expire in 10 minutes.'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [email]
    
#     try:
#         send_mail(subject, message, from_email, recipient_list)
#         return True
#     except Exception as e:
#         print(f"Failed to send email: {str(e)}")
#         return False

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # User won't be able to log in until OTP is verified
#             user.save()
            
#             # Generate and save OTP
#             otp = generate_otp()
#             user.otp = otp
#             user.otp_created_at = timezone.now()
#             user.save()
            
#             # Send OTP via email
#             if send_otp_email(user.email, otp):
#                 request.session['user_id'] = user.id
#                 messages.success(request, 'Registration successful. Please check your email for the OTP.')
#                 return redirect('verify_otp')
#             else:
#                 user.delete()  # Delete the user if email sending fails
#                 messages.error(request, 'Failed to send OTP. Please try again.')
#         else:
#             messages.error(request, 'Invalid form submission. Please correct the errors.')
#     else:
#         form = UserRegistrationForm()
    
#     return render(request, 'users/register.html', {'form': form})

# def verify_otp(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, 'Invalid session. Please register again.')
#         return redirect('register')
    
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         messages.error(request, 'User not found. Please register again.')
#         return redirect('register')
    
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         if not otp:
#             messages.error(request, 'Please enter the OTP.')
#         elif user.otp != otp:
#             messages.error(request, 'Invalid OTP. Please try again.')
#         elif not user.is_otp_valid():
#             messages.error(request, 'OTP has expired. Please request a new one.')
#         else:
#             user.is_active = True
#             user.otp = None
#             user.otp_created_at = None
#             user.save()
#             login(request, user)
#             messages.success(request, 'OTP verified successfully. You are now logged in.')
#             return redirect('home')  # Redirect to home page or dashboard
    
#     return render(request, 'users/verify_otp.html')

# def resend_otp(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         messages.error(request, 'Invalid session. Please register again.')
#         return redirect('register')
    
#     try:
#         user = User.objects.get(id=user_id)
#     except User.DoesNotExist:
#         messages.error(request, 'User not found. Please register again.')
#         return redirect('register')
    
#     otp = generate_otp()
#     user.otp = otp
#     user.otp_created_at = timezone.now()
#     user.save()
    
#     if send_otp_email(user.email, otp):
#         messages.success(request, 'A new OTP has been sent .')
#     else:
#         messages.error(request, 'Failed to send new OTP. Please try again.')
    
#     return redirect('verify_otp')









