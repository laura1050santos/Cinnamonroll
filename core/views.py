from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (
    Produto,
    Pedido,
    Perfil,
    ItemCarrinho,
    ItemPedido,
    Carrinho
)

from .forms import (
    ProdutoForm,
    PedidoForm,
    PerfilForm,
    ItemCarrinhoForm,
    ItemPedidoForm,
    CarrinhoForm
)
def homepage(request):
    return render(request, 'core/homepage.html')

def searchpage(request):
    return render(request, 'core/searchpage.html')

def login(request):
    return render(request, 'core/login.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')

def editar_produto(request,id):
    produto = get_object_or_404(Produto,id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('core/produto.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def perfilCliente_listar(request):
    perfis = Perfil.objects.filter(tipo="CLIENTE")

    return render(request, 'core/perfilCliente_listar.html', {
        'perfis': perfis
    })


@login_required
def perfilCliente(request, id):
    perfil = get_object_or_404(
        Perfil,
        id=id,
        tipo="CLIENTE"
    )

    return render(request, 'core/perfilCliente.html', {
        'perfil': perfil
    })


@login_required
def perfilCliente_criar(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)

        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.tipo = "CLIENTE"
            perfil.save()

            return redirect('perfilCliente_listar')
    else:
        form = PerfilForm()

    return render(request, 'core/perfilCliente_form.html', {
        'form': form
    })

@login_required
def perfilCliente_editar(request, id):
    perfil = get_object_or_404( Perfil,id=id,tipo="CLIENTE")
    if request.method == 'POST':
        form = PerfilForm(request.POST,request.FILES,instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.tipo = "CLIENTE"
            perfil.save()
            return redirect('perfilCliente', id=perfil.id)
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'core/perfilCliente_form.html', {'form': form, 'perfil': perfil })


@login_required
def perfilCliente_excluir(request, id):
    perfil = get_object_or_404(
        Perfil,
        id=id,
        tipo="CLIENTE"
    )
    if request.method == 'POST':
        perfil.delete()
        return redirect('perfilCliente_listar')
    return render(request, 'core/perfilCliente_confirmar_exclusao.html', {'perfil': perfil })


# PERFIL VENDEDOR

@login_required
def perfilVendedor_listar(request):
    perfis = Perfil.objects.filter(tipo="VENDEDOR")
    return render(request, 'core/perfilVendedor_listar.html', {     'perfis': perfis})

@login_required
def perfilVendedor(request, id):
    perfil = get_object_or_404(
        Perfil,
        id=id,
        tipo="VENDEDOR"
    )
    return render(request, 'core/perfilVendedor.html', {'perfil': perfil})

@login_required
def perfilVendedor_criar(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES)

        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.tipo = "VENDEDOR"
            perfil.save()

            return redirect('perfilVendedor_listar')
    else:
        form = PerfilForm()

    return render(request, 'core/perfilVendedor_form.html', {'form': form })


@login_required
def perfilVendedor_editar(request, id):
    perfil = get_object_or_404(
        Perfil,
        id=id,
        tipo="VENDEDOR"
    )

    if request.method == 'POST':
        form = PerfilForm(
            request.POST,
            request.FILES,
            instance=perfil
        )

        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.tipo = "VENDEDOR"
            perfil.save()

            return redirect('perfilVendedor', id=perfil.id)
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'core/perfilVendedor_form.html', {'form': form,'perfil': perfil})


@login_required
def perfilVendedor_excluir(request, id):
    perfil = get_object_or_404(
        Perfil,
        id=id,
        tipo="VENDEDOR"
    )

    if request.method == 'POST':
        perfil.delete()
        return redirect('perfilVendedor_listar')

    return render(request, 'core/perfilVendedor_confirmar_exclusao.html', {'perfil': perfil})

@login_required
def perfilAdmin(request, id):
    return render(request, 'core/perfilAdmin.html')

@login_required
def cardapio(request):
    return render(request, 'core/cardapio.html')

@login_required
def produto_listar(request):
    produtos = Produto.objects.all()
    return render(request, 'core/produto_listar.html', {
        'produtos': produtos
    })

#PRODUTO
@login_required
def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produto_listar')
    else:
        form = ProdutoForm()
    return render(request, 'core/produto_form.html', {'form': form})

@login_required
def produto_editar(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produto_listar')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'core/produto_form.html', {'form': form,'produto': produto})


@login_required
def produto_excluir(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_listar')
    return render(request, 'core/produto_confirmar_exclusao.html', {'produto': produto })

@login_required
def produto_detalhes(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'core/produto.html', { 'produto': produto})

@login_required
def carrinho_listar(request):
    carrinhos = Carrinho.objects.all()
    return render(request, 'core/carrinho_listar.html', {'carrinhos': carrinhos})

#ITEM_CARRINHO
@login_required
def item_carrinho_listar(request):
    itens = ItemCarrinho.objects.all()
    return render(request, 'core/item_carrinho_listar.html', {'itens': itens})

@login_required
def item_carrinho_criar(request):
    if request.method == 'POST':
        form = ItemCarrinhoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_carrinho_listar')
    else:
        form = ItemCarrinhoForm()
    return render(request, 'core/item_carrinho_form.html', {'form': form})

@login_required
def item_carrinho_editar(request, id):
    item = get_object_or_404(ItemCarrinho, id=id)
    if request.method == 'POST':
        form = ItemCarrinhoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_carrinho_listar')
    else:
        form = ItemCarrinhoForm(instance=item)
    return render(request, 'core/item_carrinho_form.html', {'form': form,'item': item})

@login_required
def item_carrinho_excluir(request, id):
    item = get_object_or_404(ItemCarrinho, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_carrinho_listar')

    return render(request, 'core/item_carrinho_confirmar_exclusao.html', {'item': item})



#PEDIDO
@login_required
def item_pedido_listar(request):
    itens = ItemPedido.objects.all()
    return render(request, 'core/item_pedido_listar.html', {
        'itens': itens })

@login_required
def item_pedido_criar(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_pedido_listar')
    else:
        form = ItemPedidoForm()
    return render(request, 'core/item_pedido_form.html', {'form': form})

@login_required
def item_pedido_editar(request, id):
    item = get_object_or_404(ItemPedido, id=id)
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_pedido_listar')
    else:
        form = ItemPedidoForm(instance=item)

    return render(request, 'core/item_pedido_form.html', {'form': form, 'item': item})

@login_required
def item_pedido_excluir(request, id):
    item = get_object_or_404(ItemPedido, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_pedido_listar')
    return render(request, 'core/item_pedido_confirmar_exclusao.html', { 'item': item})