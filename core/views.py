from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Produto,Pedido,Perfil,ItemCarrinho,ItemPedido,Carrinho
from .forms import *

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
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo')

        usuario = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Perfil.objects.create(
            usuario=usuario,
            tipo=tipo
        )

        return redirect('login')

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

    return render(request, 'core/perfilVendedor.html', {
        'perfil': perfil
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
def carrinho(request, id):
    carrinho = get_object_or_404(Carrinho, id=id)

    return render(request, 'core/carrinho.html', {
        'carrinho': carrinho
    })

@login_required
def pedido(request, id):
    return render(request, 'core/pedido.html')