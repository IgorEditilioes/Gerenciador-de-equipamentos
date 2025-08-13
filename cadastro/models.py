from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Unidade(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    n_cnes = models.IntegerField()

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    nome = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    unidade = models.ForeignKey(
        Unidade, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="funcionarios"
    )

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']

    def __str__(self):
        return self.nome
