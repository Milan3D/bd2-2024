from django.db import models


class Armazem(models.Model):
    id_armazem = models.IntegerField(primary_key=True)
    nome_armazem = models.TextField()
    morada_armazem = models.TextField()
    email_armazem = models.TextField()
    contacto_armazem = models.DecimalField(max_digits=9, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'armazem'


class Categoriacomponentes(models.Model):
    id_catcomponentes = models.IntegerField(primary_key=True)
    nome_catcomponentes = models.TextField()
    descricao_catcomponentes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoriacomponentes'


class Clientes(models.Model):
    id_cliente = models.IntegerField(primary_key=True)
    nome_cliente = models.TextField()
    datanasc_cliente = models.DateField()
    morada_cliente = models.TextField()
    nif_cliente = models.IntegerField()
    email_cliente = models.TextField()
    contacto_cliente = models.DecimalField(max_digits=9, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'clientes'


class Componentes(models.Model):
    id_componente = models.IntegerField(primary_key=True)
    id_catcomponentes = models.ForeignKey(Categoriacomponentes, models.DO_NOTHING, db_column='id_catcomponentes')
    nome_componente = models.TextField()
    descricao_componente = models.TextField(blank=True, null=True)
    precomedio_componente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'componentes'


class Encomendas(models.Model):
    id_encomenda = models.IntegerField(primary_key=True)
    id_guiacompras = models.ForeignKey('Guiaremessacompras', models.DO_NOTHING, db_column='id_guiacompras', blank=True, null=True)
    data_encomenda = models.DateField()

    class Meta:
        managed = False
        db_table = 'encomendas'


class EncomendasComponentes(models.Model):
    id_encomenda = models.OneToOneField(Encomendas, models.DO_NOTHING, db_column='id_encomenda', primary_key=True)  # The composite primary key (id_encomenda, id_componente) found, that is not supported. The first column is selected.
    id_componente = models.ForeignKey(Componentes, models.DO_NOTHING, db_column='id_componente')
    quantidade_ec = models.IntegerField()
    precounidade_ec = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'encomendas_componentes'
        unique_together = (('id_encomenda', 'id_componente'),)


class Equipamentos(models.Model):
    id_equip = models.IntegerField(primary_key=True)
    id_tipoequip = models.ForeignKey('Tipoequipamentos', models.DO_NOTHING, db_column='id_tipoequip')
    id_mo = models.ForeignKey('Maodeobra', models.DO_NOTHING, db_column='id_mo', blank=True, null=True)
    nome_equip = models.TextField()
    desc_equip = models.TextField(blank=True, null=True)
    custo_equip = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'equipamentos'


class EquipamentosFatura(models.Model):
    id_fatura = models.OneToOneField('Fatura', models.DO_NOTHING, db_column='id_fatura', primary_key=True)  # The composite primary key (id_fatura, id_equip) found, that is not supported. The first column is selected.
    id_equip = models.ForeignKey(Equipamentos, models.DO_NOTHING, db_column='id_equip')
    quantidade_equipfatura = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'equipamentos_fatura'
        unique_together = (('id_fatura', 'id_equip'),)


class Fatura(models.Model):
    id_fatura = models.IntegerField(primary_key=True)
    id_guiavendas = models.ForeignKey('Guiaremessavendas', models.DO_NOTHING, db_column='id_guiavendas', blank=True, null=True)
    id_cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='id_cliente')
    preco_fatura = models.DecimalField(max_digits=10, decimal_places=2)
    data_fatura = models.DateField()

    class Meta:
        managed = False
        db_table = 'fatura'


class Fornecedores(models.Model):
    id_fornecedor = models.IntegerField(primary_key=True)
    nome_fornecedor = models.TextField()
    morada_fornecedor = models.TextField()
    email_fornecedor = models.TextField()
    contacto_fornecedor = models.DecimalField(max_digits=9, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'fornecedores'


class FornecedoresComponentes(models.Model):
    id_componente = models.OneToOneField(Componentes, models.DO_NOTHING, db_column='id_componente', primary_key=True)  # The composite primary key (id_componente, id_fornecedor) found, that is not supported. The first column is selected.
    id_fornecedor = models.ForeignKey(Fornecedores, models.DO_NOTHING, db_column='id_fornecedor')

    class Meta:
        managed = False
        db_table = 'fornecedores_componentes'
        unique_together = (('id_componente', 'id_fornecedor'),)


class Guiaremessacompras(models.Model):
    id_guiacompras = models.IntegerField(primary_key=True)
    id_armazem = models.ForeignKey(Armazem, models.DO_NOTHING, db_column='id_armazem')
    data_guiacompras = models.DateField()

    class Meta:
        managed = False
        db_table = 'guiaremessacompras'


class Guiaremessavendas(models.Model):
    id_guiavendas = models.IntegerField(primary_key=True)
    id_armazem = models.ForeignKey(Armazem, models.DO_NOTHING, db_column='id_armazem')
    data_guiavendas = models.DateField()

    class Meta:
        managed = False
        db_table = 'guiaremessavendas'


class Maodeobra(models.Model):
    id_mo = models.IntegerField(primary_key=True)
    nome_mo = models.TextField()
    desc_mo = models.TextField(blank=True, null=True)
    custo_mo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'maodeobra'


class Receitaequip(models.Model):
    id_equip = models.OneToOneField(Equipamentos, models.DO_NOTHING, db_column='id_equip', primary_key=True)  # The composite primary key (id_equip, id_componente) found, that is not supported. The first column is selected.
    id_componente = models.ForeignKey(Componentes, models.DO_NOTHING, db_column='id_componente')
    quantidade_receita = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receitaequip'
        unique_together = (('id_equip', 'id_componente'),)


class Stockcomponentes(models.Model):
    id_armazem = models.OneToOneField(Armazem, models.DO_NOTHING, db_column='id_armazem', primary_key=True)  # The composite primary key (id_armazem, id_componente) found, that is not supported. The first column is selected.
    id_componente = models.ForeignKey(Componentes, models.DO_NOTHING, db_column='id_componente')
    quantidade_stockcomp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stockcomponentes'
        unique_together = (('id_armazem', 'id_componente'),)


class Stockequipamentos(models.Model):
    id_armazem = models.OneToOneField(Armazem, models.DO_NOTHING, db_column='id_armazem', primary_key=True)  # The composite primary key (id_armazem, id_equip) found, that is not supported. The first column is selected.
    id_equip = models.ForeignKey(Equipamentos, models.DO_NOTHING, db_column='id_equip')
    quantidade_stockequip = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stockequipamentos'
        unique_together = (('id_armazem', 'id_equip'),)


class Tipoequipamentos(models.Model):
    id_tipoequip = models.IntegerField(primary_key=True)
    nome_tipoequip = models.TextField()
    desc_tipoequip = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipoequipamentos'
