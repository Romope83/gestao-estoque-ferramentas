# produtos/forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        # Define os campos que aparecerão no formulário
        fields = ['nome', 'descricao', 'quantidade_estoque', 'estoque_minimo', 'especificacoes']