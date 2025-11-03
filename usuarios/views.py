# usuarios/views.py
from django.shortcuts import render
# Decorator para garantir que o usuário esteja logado para ver esta página
from django.contrib.auth.decorators import login_required 

@login_required # Protege esta view
def principal(request):
    # Passamos o nome do usuário para o template
    context = {
        'usuario': request.user 
    }
    return render(request, 'principal.html', context)