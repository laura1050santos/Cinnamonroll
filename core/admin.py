from django.contrib import admin
from django.contrib.auth.models import Group


cliente_group, _ = Group.objects.get_or_create(
    name="Clientes"
)

vendedor_group, _ = Group.objects.get_or_create(
    name="Vendedores"
)

admin_group, _ = Group.objects.get_or_create(
    name="Administradores"
)