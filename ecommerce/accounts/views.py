from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils import timezone
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegistrationForm

def login_view(request):
    next_page = request.GET.get('next', 'shop:product_list')
    if request.user.is_authenticated:
        return redirect(next_page)
    
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data.get('remember_me', False)
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            messages.success(request, 'Login successful!')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login_new.html', {'form': form})


def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('shop:product_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')
        
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            user = form.save()
            
            # Send welcome email
            try:
                context = {
                    'user': user,
                    'site_url': settings.SITE_URL.rstrip('/'),
                    'STATIC_URL': settings.STATIC_URL,
                    'current_year': timezone.now().year
                }
                
                html_message = render_to_string('accounts/email/welcome.html', context)
                plain_message = strip_tags(html_message)
                
                email = EmailMultiAlternatives(
                    subject='Welcome to Swiftbuy!',
                    body=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
                
                messages.success(request, 'Account created successfully! Please check your email for confirmation.')
                auth_login(request, user)
                return redirect('shop:product_list')
                
            except Exception as e:
                print(f"Error sending welcome email: {str(e)}")
                messages.warning(request, 'Account created successfully, but we could not send the welcome email.')
                auth_login(request, user)
                return redirect('shop:product_list')
                
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            messages.error(request, 'An error occurred while creating your account. Please try again.')
            
    return render(request, 'accounts/register.html', {'form': form})
                
                send_mail(
                    subject='Welcome to Swiftbuy!',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message
                )
                print(f"Welcome email sent to {user.email}")
            except Exception as e:
                # Log the error but don't fail registration
                print(f"Error sending welcome email: {str(e)}")
            
            # Login user and redirect
            auth_login(request, user)
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')


def main_page(request):
    return render(request, 'index.u.html', {'user': request.user})