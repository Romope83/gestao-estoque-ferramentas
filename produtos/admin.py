# produtos/admin.py
from django.contrib import admin
from .models import Produto, MovimentacaoEstoque

# Classe para mostrar mais detalhes na lista do admin
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_estoque', 'estoque_minimo', 'abaixo_do_minimo')
    search_fields = ('nome', 'descricao') # Campo de busca (Requisito Entrega 6)

class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'data', 'responsavel')
    list_filter = ('tipo', 'data')
    autocomplete_fields = ('produto', 'responsavel') # Facilita a busca

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(MovimentacaoEstoque, MovimentacaoEstoqueAdmin)