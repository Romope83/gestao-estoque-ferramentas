# produtos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto, MovimentacaoEstoque
from .forms import ProdutoForm
# Importa o Q para buscas complexas (usado no campo de busca)
from django.db.models import Q 

# --- ENTREGA 6: CRUD de Produtos ---

@login_required
def lista_produtos(request):
    # Lógica de Busca (Requisito)
    query = request.GET.get('busca', '') # Pega o parâmetro 'busca' da URL
    
    if query:
        # Filtra produtos pelo nome OU descrição
        produtos_list = Produto.objects.filter(
            Q(nome__icontains=query) | Q(descricao__icontains=query)
        )
    else:
        produtos_list = Produto.objects.all()

    context = {
        'produtos': produtos_list,
        'query': query
    }
    return render(request, 'produtos/lista_produtos.html', context)


@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid(): # Validação de dados (Requisito)
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
        
    # Alertas de erro são tratados pelo 'form' no template
    return render(request, 'produtos/form_produto.html', {'form': form, 'titulo': 'Novo Produto'})


@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk) # Busca o produto ou retorna 404
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produtos/form_produto.html', {'form': form, 'titulo': 'Editar Produto'})


@login_required
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    # Usamos POST para exclusão por segurança
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    
    # Se não for POST, mostramos a confirmação
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})


# --- ENTREGA 7: Gestão de Estoque ---

@login_required
def gestao_estoque(request):
    # Listar em ordem alfabética (Requisito)
    produtos_list = Produto.objects.order_by('nome') 
    
    # O alerta de estoque mínimo será feito no template
    context = {
        'produtos': produtos_list
    }
    return render(request, 'produtos/gestao_estoque.html', context)


@login_required
def movimentar_estoque(request, pk):
    # Esta view só aceita POST
    if request.method == 'POST':
        produto = get_object_or_404(Produto, pk=pk)
        
        # Pega os dados do formulário da tela 'gestao_estoque'
        try:
            # Garante que a quantidade é um número positivo
            quantidade = int(request.POST.get('quantidade'))
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser positiva")
        except (ValueError, TypeError):
            # Lidar com erro de input (opcional, mas bom)
            return redirect('gestao_estoque') 

        tipo_mov = request.POST.get('tipo') # 'E' para Entrada, 'S' para Saída

        # Lógica de movimentação
        if tipo_mov == 'E':
            produto.quantidade_estoque += quantidade
        elif tipo_mov == 'S':
            if produto.quantidade_estoque >= quantidade:
                produto.quantidade_estoque -= quantidade
            else:
                # Opcional: lidar com erro de estoque insuficiente
                print("Erro: Tentativa de saída maior que o estoque.")
                # Você pode adicionar uma mensagem de erro aqui
                return redirect('gestao_estoque')

        produto.save() # Salva a nova quantidade no produto

        # Registra o histórico (Requisito)
        MovimentacaoEstoque.objects.create(
            produto=produto,
            quantidade=quantidade,
            tipo=tipo_mov,
            responsavel=request.user, # Pega o usuário logado
            # Data é automática (auto_now_add=True no model)
        )
        
    return redirect('gestao_estoque') # Volta para a tela de gestão