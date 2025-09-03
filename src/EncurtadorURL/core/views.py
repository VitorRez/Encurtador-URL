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
from .database.repositories.usuario import *
from .database.repositories.short_url import *


# Create your views here.


def create_refresh(id):
    refresh = RefreshToken()

    refresh["user_id"] = id
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
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = verify_password(email, password)

    if user == None:
        return {'error': 'Email ou senha inválidos.'}

    refresh = create_refresh(user['id'])

    request.session['refresh'] = str(refresh)
    request.session['access'] = str(refresh.access_token)
    request.session['user_id'] = user['id']

    return {'message': 'Login realizado com sucesso.'}


def encurtar_view(request):
    user_id = request.session.get('user_id')

    original_url = request.POST.get('original_url')
    custom_url = request.POST.get('custom_url')

    response = create_short_url(original_url, user_id, custom_url)
    return response


def homepage_view(request):
    user_id = request.session.get('user_id')
    token = verify_token(request)
    username = ''

    if user_id:
        user = get_user_by_id(user_id)
        if user:
            username = user.get('username', '')

    urls = get_short_urls()
    
    context = {
        'urls': urls,
        'is_authenticated': bool(token),
        'username': username
    }

    if request.method == 'POST':
        if request.POST.get('email'):
            response = login_view(request)
            token = verify_token(request)
            context.update({
                'response': response,
                'is_authenticated': bool(token)
            })

        elif request.POST.get('original_url'):
            response = encurtar_view(request)
            urls = get_short_urls()
            context.update({
                'urls': urls,
                'response': response
            })

        elif request.POST.get('new_username'):
            response = perfil_view(request)
            urls = get_short_urls()
            context.update({
                'urls': urls,
                'response': response
            })

    return render(request, 'core/home.html', context)


def usuarios_view(request):
    token = verify_token(request)

    if not token:
        return redirect('homepage')
    
    response = {}

    if request.method == 'POST':
        new_username = request.POST['new_username']
        new_email = request.POST['new_email']
        new_password = generate_code(8)

        response = create_user(new_username, new_email, new_password)

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

    return render(request, 'core/usuarios.html', {'users': users, 'response': response})

def perfil_view(request):
    user_id = request.session.get('user_id')
    user = get_user_by_id(user_id)
    
    new_username = request.POST['new_username']
    new_email = request.POST['new_email']
    new_password = request.POST['new_password']
    new_password_2 = request.POST['new_password_2']
    password = request.POST['password']

    if not verify_password(user['email'], password):
        return {'error': 'Senha incorreta.'}
        
    if new_password and new_password != new_password_2:
        return {'error': 'As senhas novas não conferem.'}
    
    response = update_user(
        user_id,
        username=new_username if new_username else None,
        email=new_email if new_email else None,
        password=new_password if new_password else None
    )


    return response

def redirecionar_view(request, code):

    try:
        url = get_short_url_by_code(code)
        update_click(code)

        return redirect(url['original_url'])
    
    except Exception as e:
        return render(request, 'core/404.html', status=404)
    
def logout_view(request):
    request.session.flush()  # limpa toda a sessão
    return redirect("/")     # redireciona para a homepage