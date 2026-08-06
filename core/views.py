from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'core/homepage.html')

def searchpage(request):
    return render(request, 'core/searchpage.html')

def login(request):
    return render(request, 'core/login.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def perfilCliente(request):
    return render(request, 'core/perfilCliente.html')

@login_required
def perfilVendedor(request):
    return render(request, 'core/perfilVendedor.html')

@login_required
def perfilAdmin(request):
    return render(request, 'core/perfilAdmin.html')

@login_required
def cardapio(request):
    return render(request, 'core/cardapio.html')

@login_required
def produto(request):
    return render(request, 'core/produto.html')

@login_required
def carrinho(request):
    return render(request, 'core/carrinho.html')

@login_required
def pedido(request):
    return render(request, 'core/pedido.html')