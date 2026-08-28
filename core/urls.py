from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', homepage, name='homepage'),
    path('searchpage/', searchpage, name='searchpage'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('cadastro/', cadastro, name='cadastro'),
    path('cadastro-loja/', cadastro_loja, name='cadastro_loja'),
    path('dashboard/', dashboard, name='dashboard'),

    path('perfilCliente/', perfilCliente, name='perfilCliente'),
    path('perfilVendedor/', perfilVendedor, name='perfilVendedor'),
    path('perfilAdmin/', perfilAdmin, name='perfilAdmin'),

    path('cardapio/', cardapio, name='cardapio'),
    path('produto/<int:id>/', produto, name='produto'),
    path('carrinho/<int:id>/', carrinho, name='carrinho'),
    path('pedido/', pedido, name='pedido'),
]
