# gestao_estoque/urls.py
from django.contrib import admin
from django.urls import path, include
# Importa as views de autenticação nativas do Django (Entrega 4)
from django.contrib.auth import views as auth_views 
# Importa as views do nosso app 'usuarios' (Entrega 5)
from usuarios import views as usuarios_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ENTREGA 4: Interface de Autenticação (Login)
    # A URL raiz ('/') vai para a view de login nativa do Django
    # Ela vai procurar o template em 'templates/registration/login.html'
    path('', auth_views.LoginView.as_view(), name='login'),

    # ENTREGA 5: Interface Principal e Logout
    path('principal/', usuarios_views.principal, name='principal'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # ENTREGA 6 e 7: Rotas dos apps de Produtos e Estoque
    # Vamos criar um arquivo urls.py dentro do app 'produtos'
    path('produtos/', include('produtos.urls')),
]