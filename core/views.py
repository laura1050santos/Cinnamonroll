from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto,Pedido,Perfil,ItemCarrinho,ItemPedido,Carrinho

def homepage(request):
    return render(request, 'core/homepage.html')

def searchpage(request):
    return render(request, 'core/searchpage.html')

def login(request):
    return render(request, 'core/login.html')

def cadastro(request):
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipo_usuario')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validações básicas e salvamento do usuário aqui...
        
        if tipo_usuario == 'vendedor':
            return redirect('cadastro_loja')
        else:
            return redirect('homepage')

    return render(request, 'core/cadastro.html')

def cadastro_loja(request):
    if request.method == 'POST':
        
        return redirect('homepage')  

    return render(request, 'core/cadastro_loja.html')

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
def perfilCliente(request, id):
    return render(request, 'core/perfilCliente.html')

@login_required
def perfilVendedor(request, id):
    return render(request, 'core/perfilVendedor.html')

@login_required
def perfilAdmin(request, id):
    return render(request, 'core/perfilAdmin.html')

@login_required
def cardapio(request):
    return render(request, 'core/cardapio.html')

@login_required
def produto(request, id):
    return render(request, 'core/produto.html')

@login_required
def carrinho(request, id):
    return render(request, 'core/carrinho.html')

@login_required
def pedido(request, id):
    return render(request, 'core/pedido.html')