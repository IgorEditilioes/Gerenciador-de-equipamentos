from django.contrib import admin
from .models import Categoria, Unidade, Funcionario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'endereco', 'n_cnes')
    list_display_links = ('nome',)
    search_fields = ('nome', 'endereco', 'n_cnes')
    ordering = ('nome',)


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cargo', 'unidade')
    search_fields = ('nome', 'cargo', 'email')
    list_filter = ('unidade',)
    ordering = ('nome',)
    list_per_page = 10