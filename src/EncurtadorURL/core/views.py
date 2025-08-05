from django.shortcuts import redirect, render
import string, random
from .models import ShortURL

# Create your views here.

def generate_code(length=6):

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def encurtar_view(request):

    if request.method == 'POST':

        original_url = request.POST['original_url']
        code = generate_code()

        while ShortURL.objects.filter(short_code=code).exists():
            code = generate_code()

        short_url = ShortURL.objects.create(original_url=original_url, short_code=code)
        return render(request, 'core/encurtador.html', {'short_url': short_url})
    
    return render(request, 'core/form.html')

def redirecionar_view(request, code):

    try:
        url = ShortURL.objects.get(short_code=code)
        url.clicks += 1
        url.save()

        return redirect(url.original_url)
    
    except ShortURL.DoesNotExist:
        return render(request, 'core/404.html', status=404)