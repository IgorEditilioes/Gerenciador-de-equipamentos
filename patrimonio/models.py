from django.db import models
from cadastro.models import Categoria, Unidade, Funcionario
from django.core.exceptions import ValidationError


class Equipamento(models.Model):
    STATUS_CHOICES = [
        ('funcionando', 'Funcionando'),
        ('defeito', 'Com defeito'),
        ('quebrado', 'Quebrado'),
        ('roubado', 'Roubado'),
        ('manutencao', 'Em manutenção'),
        ('em estoque', 'Em estoque'),
        ('fora de estoque', 'Fora de estoque'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='funcionando',
        help_text="Situação atual do equipamento"
    )
    
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    numero_patrimonio = models.CharField(max_length=50, blank=True, null=True, unique=True)
    descricao = models.TextField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    funcionario = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='equipamentos'
    )
    unidade = models.ForeignKey(
        Unidade, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='equipamentos'
    )

    quantidade_estoque = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos" 
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} (Patrimônio: {self.numero_patrimonio or 'Sem número'})"


class Movimentacao(models.Model):
    equipamento = models.ForeignKey(
        Equipamento, on_delete=models.CASCADE,
        related_name='movimentacoes'
    )
    data_movimentacao = models.DateTimeField(auto_now_add=True)

    origem_funcionario = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='movimentacoes_origem'
    )
    destino_funcionario = models.ForeignKey(
        Funcionario, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='movimentacoes_destino'
    )
    origem_unidade = models.ForeignKey(
        Unidade, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='movimentacoes_origem'
    )
    destino_unidade = models.ForeignKey(
        Unidade, on_delete=models.SET_NULL, blank=True, null=True,
        related_name='movimentacoes_destino'
    )

    quantidade = models.PositiveIntegerField(default=1)
    observacao = models.TextField(blank=True, null=True)

    TIPO_MOVIMENTACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO)

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        ordering = ['-data_movimentacao']

    def clean(self):
        super().clean()
        if self.tipo == 'saida':
            if self.equipamento_id is None:
                return
            if self.equipamento.quantidade_estoque < self.quantidade:
                raise ValidationError(f'Estoque insuficiente: há {self.equipamento.quantidade_estoque} unidades disponíveis, mas tentou retirar {self.quantidade}.')

    def __str__(self):
        if self.equipamento_id:
            return f"Movimentação do {self.equipamento.nome} em {self.data_movimentacao.strftime('%Y-%m-%d %H:%M')}"
        return "Movimentação (sem equipamento)"

    def save(self, *args, **kwargs):
        self.full_clean()  # valida antes de salvar
        is_new = self.pk is None
        super().save(*args, **kwargs)

        equipamento = self.equipamento

        # Só atualiza se houver número de patrimônio
        if equipamento.numero_patrimonio:
            # Atualiza estoque
            if self.tipo == 'saida':
                equipamento.quantidade_estoque = max(0, equipamento.quantidade_estoque - self.quantidade)
            else:  # entrada
                equipamento.quantidade_estoque += self.quantidade

            # Atualiza unidade do equipamento se houver destino
            if self.destino_unidade:
                equipamento.unidade = self.destino_unidade

            equipamento.save()