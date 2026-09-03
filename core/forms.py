from django import forms
from .models import Perfil, Produto, ItemCarrinho, Pedido


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'tipo',
            'telefone',
            'endereco',
            'nome_loja',
            'descricao_loja',
            'foto'
        ]


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'preco',
            'estoque',
            'imagem'
        ]


class ItemCarrinhoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrinho
        fields = [
            'produto',
            'quantidade'
        ]


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'status'
        ]

