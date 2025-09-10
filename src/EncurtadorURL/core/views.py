from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
import string, random
from .models import ShortURL


# Create your views here.

def verify_token(request):
    token_str = request.session.get('access')
    if not token_str:
        return None
    try:
        return AccessToken(token_str)
    except TokenError:
        return None

def generate_code(length=6):

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def login_view(request):
    email = request.POST.get('email')   
    password = request.POST.get('password')

    try:
        user = get_user_model().objects.get(email=email)

    except get_user_model().DoesNotExist:
        return {'error': 'Email inválido.'}

    user = authenticate(request, username=user.username, password=password)

    if not user:
        return {'error': 'Usuário ou senha inválidos.'}

    refresh = RefreshToken.for_user(user)

    request.session['refresh'] = str(refresh)
    request.session['access'] = str(refresh.access_token)
    request.session['user_id'] = user.id

    return {'message': 'Login realizado com sucesso.'}


def encurtar_view(request):
    user_id = request.session.get('user_id')

    original_url = request.POST.get('original_url')
    custom_url = request.POST.get('custom_url')

    User = get_user_model()
    user = User.objects.get(id=user_id)

    try:
        short_code = custom_url if custom_url else generate_code()

        short_url = ShortURL.objects.create(
            short_code=short_code,
            original_url=original_url,
            usuario=user
        )

        return {"message": "URL encurtada com sucesso.", "short_code": short_url.short_code}

    except Exception as e:
        return {"error": "URL customizada já foi usada ou ocorreu um erro."}


def homepage_view(request):
    user_id = request.session.get('user_id')
    token = verify_token(request)

    urls = ShortURL.objects.all().order_by('-created_at')
    
    context = {
        'urls': urls,
        'is_authenticated': bool(token),
        'user_id': user_id
    }

    if request.method == 'POST':
        if request.POST.get('email'):
            response = login_view(request)

        elif request.POST.get('original_url'):
            response = encurtar_view(request)

        elif request.POST.get('new_username'):
            response = perfil_view(request)

        if 'message' in response:
            messages.success(request, response['message'])
        if 'error' in response:
            messages.error(request, response['error'])

        return redirect('homepage')

    return render(request, 'core/home.html', context)


def usuarios_view(request):
    token = verify_token(request)

    if not token:
        return redirect('homepage')

    User = get_user_model()

    if request.method == 'POST':
        new_username = request.POST['new_username']
        new_email = request.POST['new_email']
        new_password = generate_code(8)

        try:
            user = User.objects.create_user(
                username=new_username,
                email=new_email,
                password=new_password
            )

        except IntegrityError:
            return {'error': 'Erro ao criar usuário: Já existe um usuário com essas credenciais.'}

        assunto = "Sua conta foi criada"
        mensagem = f"Olá {new_username},\n\nSua conta foi criada com sucesso.\nSua senha é: {new_password}\n\nPor segurança, altere-a após o login."
        
        send_mail(
            assunto,
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [new_email],
            fail_silently=False,
        )

    users = User.objects.all().order_by('-id')

    return render(request, 'core/usuarios.html', {'users': users})

def perfil_view(request):
    user_id = request.session.get('user_id')
    user = user = get_user_model().objects.get(id=user_id)

    if not check_password(request.POST['password'], user.password):
        return {'error': 'Senha incorreta.'}
        
    if request.POST['new_password'] and request.POST['new_password'] != request.POST['new_password_2']:
        return {'error': 'As senhas novas não conferem.'}
    
    if request.POST.get('new_username'):
        user.username = request.POST['new_username']
    if request.POST.get('new_email'):
        user.email = request.POST['new_email']
    if request.POST.get('new_password'):
        user.password = make_password(request.POST['new_password'])

    user.save()

    return {'message': 'Usuário atualizado com sucesso'}


def redirecionar_view(request, code):

    try:
        url = ShortURL.objects.get(short_code=code)
        url.clicks += 1
        url.save()

        return redirect(url.original_url)
    
    except Exception as e:
        return render(request, 'core/404.html', status=404)
    
def logout_view(request):
    request.session.flush()  # limpa toda a sessão
    return redirect("/")     # redireciona para a homepage