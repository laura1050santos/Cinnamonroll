from django.contrib import admin
from .models import (
    Perfil,
    Produto,
    Carrinho,
    ItemCarrinho,
    Pedido,
    ItemPedido
)

admin.site.register(Perfil)
admin.site.register(Produto)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(Pedido)
admin.site.register(ItemPedido)