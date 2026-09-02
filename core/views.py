from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Produto,Pedido,Perfil,ItemCarrinho,ItemPedido,Carrinho
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

def get_image(request, obj_id):
    if not request.session:
        return HttpResponseForbidden()

    obj = objetos_rep.get_objeto(obj_id)

    if not obj or not obj.photo:
        return HttpResponse("Imagem não encontrada", status=404)

    photo = obj.photo
    photo_header = photo[:8]

    # JPEG
    if photo_header[:2] == b"\xFF\xD8":
        mime_type = "image/jpeg"

    # PNG
    elif photo_header[:4] == b"\x89\x50\x4E\x47":
        mime_type = "image/png"

    # GIF
    elif photo_header[:6] in (b"GIF87a", b"GIF89a"):
        mime_type = "image/gif"

    else:
        return HttpResponse(
            "Formato de imagem não suportado",
            status=400
        )

    return HttpResponse(
        photo,
        content_type=mime_type
    )

def homepage(request):
    return render(request, 'core/homepage.html')

def searchpage(request):
    return render(request, 'core/searchpage.html')


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

        # Faz login automaticamente
        login(request, usuario)

        # Se for vendedor, vai para cadastro da loja
        if tipo == 'VENDEDOR':
            return redirect('cadastro_loja')

        # Se for cliente, vai para a homepage
        return redirect('homepage')

    return render(request, 'core/cadastro.html')


@login_required
def cadastro_loja(request):

    perfil = request.user.perfil

    # Garante que somente vendedores possam acessar
    if perfil.tipo != 'VENDEDOR':
        return redirect('homepage')

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
def perfilVendedor(request):
    perfil = request.user.perfil

    if perfil.tipo != "VENDEDOR":
        return redirect('homepage')

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
    return render(request, 'core/cardapio.html')

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
def pedido(request, id):
    return render(request, 'core/pedido.html')

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

#cadastro de produtos pelo vendedor

@login_required
def cadastrar_produto(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if perfil.tipo != "VENDEDOR":
        return redirect('homepage')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        estoque = request.POST.get('estoque')
        imagem = request.FILES.get('imagem')

        # Cria o produto relacionando ao vendedor (perfil)
        Produto.objects.create(
            vendedor=perfil,
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            imagem=imagem
        )
        return redirect('perfil_vendedor')

    return render(request, 'core/cadastrarProdutos.html')

@login_required
def editar_loja(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        perfil.nome_loja = request.POST.get('nome_loja')
        perfil.descricao_loja = request.POST.get('descricao_loja')
        perfil.telefone = request.POST.get('telefone')
        perfil.endereco = request.POST.get('endereco')

        # Atualiza a foto somente se o usuário tiver selecionado um novo arquivo
        if request.FILES.get('foto'):
            perfil.foto = request.FILES.get('foto')

        perfil.save()
        return redirect('perfil_vendedor')

    return render(request, 'core/editarloja.html', {'perfil': perfil})

def consultar_loja(request, loja_id):
    loja = get_object_or_404(Perfil, pk=loja_id)
    produtos = loja.produtos.all()

    return render(request, 'core/minhaloja.html', {
        'loja': loja,
        'produtos': produtos
    })

@login_required
def perfil_vendedor(request):
    # Busca o perfil vinculado ao usuário logado
    perfil, created = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={'tipo': 'VENDEDOR'}  # Caso não exista, define como VENDEDOR
    )

    # Verifica se o tipo é diferente de VENDEDOR (em maiúsculo!)
    if perfil.tipo != "VENDEDOR":
        return redirect('homepage')

    # Busca os produtos onde o campo vendedor é o perfil atual
    produtos = perfil.produtos.all()

    return render(request, 'core/perfilVendedor.html', {
        'perfil': perfil,
        'produtos': produtos
    })

def sair(request):
    logout(request)
    return redirect('homepage')