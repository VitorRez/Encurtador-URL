from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
import string, random
from .models import ShortURL
from .database.repositories.usuario import *
from .database.repositories.short_url import *

# Create your views here.

def generate_code(length=6):

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_refresh(username):
    refresh = RefreshToken()

    refresh['username'] = username
    
    refresh.set_exp(from_time=now(), lifetime=timedelta(days=1))
    refresh.access_token.set_exp(from_time=now(), lifetime=timedelta(minutes=30))

    return refresh

def login_view(request):
    if request.method != 'POST':
        return render(request, 'core/login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = verify_password(username, password)

    if user is None:
        return render(request, 'core/login.html', {'error': 'Usuário ou senha inválidos'})

    refresh = create_refresh(username)

    request.session['access'] = str(refresh.access_token)
    request.session['refresh'] = str(refresh)
    request.session['user'] = username

    return redirect('encurtar')


def encurtar_view(request):
    token_str = request.session.get('access')

    if not token_str:
        return redirect('login')
    
    try:
        token = AccessToken(token_str)
    except TokenError:
        return redirect('login')

    if request.method == 'POST':
        original_url = request.POST['original_url']
        custom_url = request.POST['custom_url']

        if custom_url:
            response = create_short_url_with_code(original_url, custom_url)
        
        else:
            response = create_short_url(original_url)

    users = get_users()
    urls = get_short_urls()
    
    return render(request, 'core/form.html', {'urls': urls, 'users': users})

def redirecionar_view(request, code):

    try:
        url = get_short_url_by_code(code)
        update_click(code)

        return redirect(url['original_url'])
    
    except ShortURL.DoesNotExist:
        return render(request, 'core/404.html', status=404)