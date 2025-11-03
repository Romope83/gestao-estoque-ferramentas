# produtos/models.py
from django.db import models
# Importa o modelo de User padrão do Django para o relacionamento
from django.contrib.auth.models import User 

class Produto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True, help_text="Detalhes, variações, material, etc.")
    
    # Campo para estoque atual
    quantidade_estoque = models.PositiveIntegerField(default=0)
    
    # Campo para o controle de estoque mínimo (Requisito)
    estoque_minimo = models.PositiveIntegerField(default=10)
    
    # O "help_text" ajuda a explicar o campo no painel admin
    especificacoes = models.TextField(blank=True, null=True, help_text="Ex: Ponta imantada, cabo isolante, material da cabeça...")

    def __str__(self):
        return self.nome
    
    # Propriedade para verificar se está abaixo do mínimo (Requisito Entrega 7)
    @property
    def abaixo_do_minimo(self):
        return self.quantidade_estoque < self.estoque_minimo


class MovimentacaoEstoque(models.Model):
    # Definindo os tipos de operação (Requisito)
    TIPO_MOVIMENTACAO = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    tipo = models.CharField(max_length=1, choices=TIPO_MOVIMENTACAO)
    data = models.DateTimeField(auto_now_add=True) # Registra data/hora automaticamente
    
    # Relacionamento com o usuário logado (Requisito)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"