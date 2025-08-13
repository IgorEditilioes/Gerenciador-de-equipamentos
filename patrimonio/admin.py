from django.contrib import admin
from .models import Equipamento, Movimentacao

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'numero_patrimonio', 'status', 'funcionario', 'unidade')
    search_fields = ('nome', 'numero_patrimonio', 'categoria__nome')
    list_filter = ('categoria', 'status', 'funcionario', 'unidade')
    ordering = ('nome',)


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipamento', 'data_movimentacao', 'origem_funcionario', 'destino_funcionario', 'origem_unidade', 'destino_unidade')
    search_fields = ('equipamento__nome',)
    list_filter = ('data_movimentacao', 'origem_unidade', 'destino_unidade', 'origem_funcionario', 'destino_funcionario')
    ordering = ('-data_movimentacao',)
