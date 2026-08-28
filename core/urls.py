from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path('searchpage/', searchpage, name='searchpage'),
    path('login/', login, name='login'),
    path('cadastro/', cadastro, name='cadastro'),
    path('cadastro-loja/', cadastro_loja, name='cadastro_loja'),
    path('dashboard/', dashboard, name='dashboard'),
    path('perfilCliente/', perfilCliente, name='perfilCliente'),
    path('perfilVendedor/', perfilVendedor, name='perfilVendedor'),
    path('perfilAdmin/', perfilAdmin, name='perfilAdmin'),
    path('cardapio/', cardapio, name='cardapio'),
    path('produto/', produto, name='produto'),
    path('carrinho/', carrinho, name='carrinho'),
    path('pedido/', pedido, name='pedido')
]