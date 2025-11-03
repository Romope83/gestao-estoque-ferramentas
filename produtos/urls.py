# produtos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Rota principal (Listagem e Busca)
    path('', views.lista_produtos, name='lista_produtos'), 
    
    # Rotas do CRUD (Inserir, Editar, Excluir)
    path('novo/', views.criar_produto, name='criar_produto'),
    path('editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),

    # Rotas da Entrega 7
    path('gestao/', views.gestao_estoque, name='gestao_estoque'),
    path('movimentar/<int:pk>/', views.movimentar_estoque, name='movimentar_estoque'),

    
]