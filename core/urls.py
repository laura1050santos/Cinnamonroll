from django.urls import path
from .views import *
<<<<<<< Updated upstream
=======
from django.contrib.auth import views as auth_views
>>>>>>> Stashed changes

urlpatterns = [
    path('', homepage, name='homepage'),
    path('searchpage/', searchpage, name='searchpage'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('dashboard/', dashboard, name='dashboard'),
    path('perfilCliente/', perfilCliente, name='perfilCliente'),
    path('perfilVendedor/', perfilVendedor, name='perfilVendedor'),
    path('perfilAdmin/', perfilAdmin, name='perfilAdmin'),
    path('cardapio/', cardapio, name='cardapio'),
<<<<<<< Updated upstream
    path('produto/', produto, name='produto'),
    path('carrinho/', carrinho, name='carrinho'),
    path('pedido/', pedido, name='pedido')
=======

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
>>>>>>> Stashed changes
]