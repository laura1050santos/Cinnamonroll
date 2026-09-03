from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Produto,Pedido,Perfil,ItemCarrinho,ItemPedido,Carrinho
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

def homepage(request):
    lojas = Perfil.objects.filter(tipo="VENDEDOR")
    return render(request, 'core/homepage.html', {'lojas': lojas})

def lojas(request):

    lojas = Perfil.objects.filter(
        tipo="VENDEDOR"
    ).exclude(
        nome_loja=""
    )

    return render(request, 'core/lojas.html', {
        'lojas': lojas
    })

def searchpage(request):
    query = request.GET.get('q', '').strip()
    produtos = []

    if query:
        produtos = Produto.objects.filter(nome__icontains=query)

    return render(request, 'core/searchpage.html', {
        'produtos': produtos,
        'query': query
    })

def cadastro(request):
    if request.method == 'POST':

        tipo_usuario = request.POST.get('tipo_usuario')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Verifica se as senhas são iguais
        if senha != confirmar_senha:
            return render(request, 'core/cadastro.html', {
                'erro': 'As senhas não coincidem.'
            })

        # Verifica se o e-mail já está cadastrado
        if User.objects.filter(username=email).exists():
            return render(request, 'core/cadastro.html', {
                'erro': 'Este e-mail já está cadastrado.'
            })

        # Converte o tipo para o formato usado no Model
        if tipo_usuario == 'vendedor':
            tipo = 'VENDEDOR'
        else:
            tipo = 'CLIENTE'

        # Cria o usuário do Django
        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )

        # Cria o perfil
        perfil = Perfil.objects.create(
            usuario=usuario,
            tipo=tipo
        )

        perfil.save()
        usuario.save()
        messages.success(
                    request,
                    'Cadastro realizado com sucesso!'
                )

        # Faz login automaticamente
        login(request, usuario)

        # Se for vendedor, vai para cadastro da loja
        if tipo == 'VENDEDOR':
            return redirect('cadastro_loja')


        # Se for cliente, vai para a perfilCliente
        return redirect('perfilCliente')

    return render(request, 'core/cadastro.html')


@login_required
def cadastro_loja(request):

    perfil = request.user.perfil

    # Garante que somente vendedores possam acessar
    if perfil.tipo != 'VENDEDOR':
        return redirect('homepage')

    if request.method == 'POST':

        perfil.nome_loja = request.POST.get('nome_loja')
        perfil.descricao_loja = request.POST.get('descricao_loja')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        

        # Salva a foto, caso tenha sido enviada
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']

        # Salva TODAS as alterações no banco
        perfil.save()

        messages.success(
            request,
            'Cadastro realizado com sucesso!'
        )

        return redirect('perfilVendedor')
    return render(request, 'core/cadastro_loja.html')

def editar_produto(request,id):
    produto = get_object_or_404(Produto,id=id)
    if request.method == 'POST':

        nome_loja = request.POST.get('nome_loja')
        descricao_loja = request.POST.get('descricao_loja')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        foto = request.FILES.get('foto')

        perfil.nome_loja = nome_loja
        perfil.descricao_loja = descricao_loja
        perfil.telefone = telefone
        perfil.endereco = endereco

        if foto:
            perfil.foto = foto

        perfil.save()

        return redirect('perfilVendedor')

    return render(request, 'core/cadastro_loja.html', {
        'perfil': perfil
    })

@login_required
def dashboard(request):
    perfil = request.user.perfil

    if perfil.tipo == "CLIENTE":
        return redirect('perfilCliente')

    elif perfil.tipo == "VENDEDOR":
        return redirect('perfilVendedor')

    elif perfil.tipo == "ADMINISTRADOR":
        return redirect('perfilAdmin')

    return HttpResponseForbidden("Tipo de usuário inválido")

@login_required
def perfilCliente(request):
    perfil = request.user.perfil

    return render(request, 'core/perfilCliente.html', {
        'perfil': perfil
    })

@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    usuario = request.user
    
    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name') # ESTE TBM N ESTÁ POIS APARECE O PRIMEIOR NOME APENAS
        usuario.email = request.POST.get('email') # EMAIL NÂO ALTERA TBM POR ALGUMA RAzão
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
            
        perfil.save()
        usuario.save()

        return redirect('perfilCliente') 
    return render(request, 'core/editarPerfilCliente.html', {'perfil': perfil})

@login_required
def excluir_perfil(request):

    if request.method == 'POST':
        usuario = request.user

        logout(request)
        usuario.delete()
        messages.success(request, "Seu perfil foi excluído com sucesso." )
        return redirect('homepage')

@login_required
def perfilVendedor(request, id=None):

    if id:
        perfil = get_object_or_404(Perfil, id=id, tipo="VENDEDOR")
    else:
        perfil = request.user.perfil

    produtos = perfil.produtos.all()

    return render(request, 'core/perfilVendedor.html', {
        'perfil': perfil,
        'produtos': produtos
    })

@login_required
def perfilAdmin(request):
    perfil = request.user.perfil

    return render(request, 'core/perfilAdmin.html', {
        'perfil': perfil
    })

@login_required
def cardapio(request):
    produtos = Produto.objects.all()

    return render(request, 'core/cardapio.html', {'produtos': produtos})

@login_required
def produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    return render(request, 'core/produto.html', {
        'produto': produto
    })

@login_required
def carrinho(request):

    perfil = request.user.perfil

    # Apenas clientes podem acessar o carrinho
    if perfil.tipo != "CLIENTE":
        return redirect('homepage')

    # Cria o carrinho automaticamente se ele ainda não existir
    carrinho, criado = Carrinho.objects.get_or_create(
        cliente=perfil
    )

    itens = carrinho.itens.select_related('produto')

    # Calcula o total
    total = sum(item.subtotal for item in itens)

    return render(request, 'core/carrinho.html', {
        'carrinho': carrinho,
        'itens': itens,
        'total': total
    })

@login_required
def aumentar_quantidade(request, id):

    perfil = request.user.perfil

    if perfil.tipo != "CLIENTE":
        return redirect('homepage')

    item = get_object_or_404(
        ItemCarrinho,
        id=id,
        carrinho__cliente=perfil
    )

    # Não deixa ultrapassar o estoque
    if item.quantidade < item.produto.estoque:
        item.quantidade += 1
        item.save()
    else:
        messages.error(
            request,
            "Não é possível adicionar mais. Estoque máximo atingido."
        )

    return redirect('carrinho')

@login_required
def diminuir_quantidade(request, id):

    perfil = request.user.perfil

    if perfil.tipo != "CLIENTE":
        return redirect('homepage')

    item = get_object_or_404(
        ItemCarrinho,
        id=id,
        carrinho__cliente=perfil
    )

    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
    else:
        item.delete()

    return redirect('carrinho')

@login_required
def remover_do_carrinho(request, id):

    perfil = request.user.perfil

    if perfil.tipo != "CLIENTE":
        return redirect('homepage')

    item = get_object_or_404(
        ItemCarrinho,
        id=id,
        carrinho__cliente=perfil
    )

    item.delete()

    messages.success(
        request,
        "Produto removido do carrinho."
    )

    return redirect('carrinho')

@login_required
def pedido(request):
    perfil = request.user.perfil

    pedidos = Pedido.objects.filter(
        cliente=perfil
    ).prefetch_related(
        'itens__produto'
    ).order_by('-data')

    for pedido in pedidos:
        pedido.total = sum(
            item.quantidade * item.preco
            for item in pedido.itens.all()
        )

    return render(request, 'core/pedidos.html', {
        'pedidos': pedidos
    })

@login_required
def finalizar_pedido(request):
    if request.method == "POST":
        # 1. Recupera o perfil do cliente logado
        perfil_cliente = request.user.perfil

        # 2. Busca o carrinho associado a esse perfil
        carrinho = Carrinho.objects.filter(cliente=perfil_cliente).first()

        # 3. Valida se o carrinho existe e tem itens
        if not carrinho or not carrinho.itens.exists():
            messages.error(request, "Seu carrinho está vazio!")
            return redirect("carrinho")

        # 4. Cria o Pedido vinculado ao Perfil
        pedido = Pedido.objects.create(
            cliente=perfil_cliente,
            status="PENDENTE"
        )

        # 5. Transfere cada ItemCarrinho para a tabela ItemPedido
        for item_carrinho in carrinho.itens.all():
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item_carrinho.produto,
                quantidade=item_carrinho.quantidade,
                preco=item_carrinho.produto.preco  # Congela o preço atual do produto
            )

        # 6. Limpa todos os itens do carrinho após criar o pedido
        carrinho.itens.all().delete()

        messages.success(request, f"Pedido #{pedido.id} realizado com sucesso!")
        return redirect("perfilCliente")  # Redireciona para a página do cliente

    # Se a requisição não for POST, redireciona de volta ao carrinho
    return redirect("carrinho")

@login_required
def pedidos_vendedor(request):
    perfil = request.user.perfil

    if perfil.tipo != "VENDEDOR":
        return redirect('homepage')

    pedidos = Pedido.objects.filter(
        itens__produto__vendedor=perfil
    ).distinct().prefetch_related(
        'itens__produto'
    ).order_by('-data')

    for pedido in pedidos:
        pedido.itens_vendedor = [
            item for item in pedido.itens.all()
            if item.produto and item.produto.vendedor == perfil
        ]

    return render(request, 'core/pedidos_vendedor.html', {
        'pedidos': pedidos
    })

@login_required
def adicionar_carrinho(request, id):

    perfil = request.user.perfil

    if perfil.tipo != "CLIENTE":
        return redirect('homepage')

    produto = get_object_or_404(Produto, id=id)

    if produto.estoque <= 0:
        messages.error(
            request,
            "Este produto está fora de estoque."
        )
        return redirect('produto', id=produto.id)

    carrinho, criado = Carrinho.objects.get_or_create(
        cliente=perfil
    )

    item, criado = ItemCarrinho.objects.get_or_create(
        carrinho=carrinho,
        produto=produto
    )

    if not criado:

        if item.quantidade < produto.estoque:
            item.quantidade += 1
            item.save()
        else:
            messages.error(
                request,
                "Não há mais unidades disponíveis em estoque."
            )

            return redirect('produto', id=produto.id)

    messages.success(
        request,
        f"{produto.nome} foi adicionado ao carrinho!"
    )

    return redirect('carrinho')

@login_required
def cadastro_produto(request):
    perfil = request.user.perfil

    if perfil.tipo != 'VENDEDOR':
        return redirect('homepage')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')
        imagem = request.FILES.get('imagem')

        produto = Produto.objects.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            imagem=imagem,
            vendedor=perfil
        )

        return redirect('perfilVendedor')
    
    return render(request, 'core/cadastro_produto.html')

@login_required
def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    return render(request, 'core/detalhe_produto.html', {
        'produto': produto
    })

@login_required
def editar_loja(request):
    perfil = request.user.perfil
        
    if request.method == 'POST':
        perfil.nome_loja = request.POST.get('nome_loja') 
        perfil.descricao_loja = request.POST.get('descricao_loja')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')
        if 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
            
        perfil.save()
        return redirect('perfilVendedor')

    return render(request, 'core/editarloja.html', {'perfil': perfil})

def sair(request):
    logout(request)
    return redirect('homepage')