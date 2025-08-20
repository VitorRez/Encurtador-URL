from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
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

def create_refresh(username):
    refresh = RefreshToken()

    refresh["username"] = username
    refresh["is_external"] = True

    return refresh

def verify_token(request):
    token_str = request.session.get('access')
    if not token_str:
        return None
    
    try:
        token = AccessToken(token_str)
        return token
    except TokenError:
        return None

def generate_code(length=6):

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def login_view(request):
    if request.method != 'POST':
        return render(request, 'core/login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = verify_password(username, password)

    if user == None:
        return render(request, 'core/login.html', {'error': 'Usuário ou senha inválidos'})

    refresh = create_refresh(username)

    request.session['refresh'] = str(refresh)
    request.session['access'] = str(refresh.access_token)
    request.session['user'] = username
    request.session['email'] = user['email']

    return redirect('homepage')

def homepage_view(request):
    token = verify_token(request)

    if not token:
        return redirect('login')

    urls = get_short_urls()
    return render(request, 'core/home.html', {'urls': urls})

def encurtar_view(request):
    token = verify_token(request)

    if not token:
        return redirect('login')
    
    username = request.session.get('user')

    if request.method == 'POST':
        
        original_url = request.POST['original_url']
        custom_url = request.POST['custom_url']

        if custom_url:
            response = create_short_url_with_code(original_url, custom_url, username)
        
        else:
            response = create_short_url(original_url, username)

    urls = get_short_urls()
    
    return render(request, 'core/form.html', {'urls': urls})

def usuarios_view(request):
    token = verify_token(request)

    if not token:
        return redirect('login')

    if request.method == 'POST':
        new_username = request.POST['new_username']
        new_email = request.POST['new_email']
        new_password = generate_code(8)

        password_hash = create_hash(new_password)
        print(new_password)

        response = create_user(new_username, new_email, password_hash)

        assunto = "Sua conta foi criada"
        mensagem = f"Olá {new_username},\n\nSua conta foi criada com sucesso.\nSua senha é: {new_password}\n\nPor segurança, altere-a após o login."
        
        send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [new_email],
            fail_silently=False,
        )


    users = get_users()

    return render(request, 'core/usuarios.html', {'users': users})

def redirecionar_view(request, code):

    try:
        url = get_short_url_by_code(code)
        update_click(code)

        return redirect(url['original_url'])
    
    except ShortURL.DoesNotExist:
        return render(request, 'core/404.html', status=404)