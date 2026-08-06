from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    TIPO_USUARIO = (
        ("CLIENTE", "Cliente"),
        ("VENDEDOR", "Vendedor"),
        ("ADMINISTRADOR", "Admin"),
    )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO)

    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)

    
    nome_loja = models.CharField(max_length=100, blank=True)
    descricao_loja = models.TextField(blank=True)
    foto = models.ImageField(upload_to="lojas/", blank=True, null=True)

    def __str__(self):
        if self.tipo == "VENDEDOR":
            return self.nome_loja
        return self.usuario.username


class Produto(models.Model):
    vendedor = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="produtos",
        limit_choices_to={"tipo": "VENDEDOR"}
    )

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)

    def __str__(self):
        return self.nome


class Carrinho(models.Model):
    cliente = models.OneToOneField(
        Perfil,
        on_delete=models.CASCADE,
        related_name="carrinho",
        limit_choices_to={"tipo": "CLIENTE"}
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrinho - {self.cliente.usuario.username}"


class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(
        Carrinho,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE
    )

    quantidade = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.quantidade * self.produto.preco


class Pedido(models.Model):
    STATUS = (
        ("PENDENTE", "Pendente"),
        ("ACEITO", "Aceito"),
        ("RECUSADO", "Recusado"),
        ("ENTREGUE", "Entregue"),
    )

    cliente = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name="pedidos",
        limit_choices_to={"tipo": "CLIENTE"}
    )

    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, default="PENDENTE")

    def __str__(self):
        return f"Pedido #{self.id}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens"
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.SET_NULL,
        null=True
    )

    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco