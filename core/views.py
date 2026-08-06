from django.shortcuts import render

def homepage(request):
    return render(request, 'core/homepage.html')

def searchpage(request):
    return render(request, 'core/searchpage.html')

def login(request):
    return render(request, 'core/login.html')

def cadastro(request):
    return render(request, 'core/cadastro.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def perfilCliente(request):
    return render(request, 'core/perfilCliente.html')

def perfilVendedor(request):
    return render(request, 'core/perfilVendedor.html')

def perfilAdmin(request):
    return render(request, 'core/perfilAdmin.html')

def cardapio(request):
    return render(request, 'core/cardapio.html')

def produto(request):
    return render(request, 'core/produto.html')

def carrinho(request):
    return render(request, 'core/carrinho.html')