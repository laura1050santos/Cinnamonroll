from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    path('', homepage, name='homepage'),
    path('searchpage/', searchpage, name='searchpage'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='core/login.html'
        ),
        name='login'
    ),

    path('logout/', sair, name='logout'),

    path('cadastro/', cadastro, name='cadastro'),
    path('cadastro-loja/', cadastro_loja, name='cadastro_loja'),
    path('cadastro-produto/', cadastrar_produto, name='cadastro_produto'),    path('dashboard/', dashboard, name='dashboard'),
    path('perfilCliente/', perfilCliente, name='perfilCliente'),
    path('perfilVendedor/', perfilVendedor, name='perfilVendedor'),
    path('perfilAdmin/', perfilAdmin, name='perfilAdmin'),
    path('excluir-perfil/',excluir_perfil, name='excluir_perfil'),


    path('cardapio/', cardapio, name='cardapio'),

    path(
        'produto/<int:id>/',
        produto,
        name='produto'
    ),

    path(
        'carrinho/',
        carrinho,
        name='carrinho'
    ),

    path(
        'carrinho/adicionar/<int:id>/',
        adicionar_carrinho,
        name='adicionar_carrinho'
    ),

    path(
        'carrinho/aumentar/<int:id>/',
        aumentar_quantidade,
        name='aumentar_quantidade'
    ),

    path(
        'carrinho/diminuir/<int:id>/',
        diminuir_quantidade,
        name='diminuir_quantidade'
    ),

    path(
        'carrinho/remover/<int:id>/',
        remover_do_carrinho,
        name='remover_do_carrinho'
    ),

    path('pedido/', pedido, name='pedido'),

    path('vendedor/loja/editar/', views.editar_loja, name='editar_loja'),
]