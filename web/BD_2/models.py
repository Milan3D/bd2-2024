from django.db import models

class acesso_pgestao(models.Model):
    id_utilpgestao = models.IntegerField(primary_key=True)
    password_pgestao = models.CharField(max_length=50)
    id_nivel = models.IntegerField(choices=[(1, 'Nível 1'), (2, 'Nível 2')], default=2)

    class Meta:
        db_table = 'acesso_pgestao'

class EquipmentItem(models.Model):
    id_equip = models.AutoField(primary_key=True)
    id_tipoequip = models.IntegerField()  # Adjust field type as necessary
    id_mo = models.IntegerField()  # Adjust field type as necessary
    nome_equip = models.CharField(max_length=255)
    desc_equip = models.TextField()
    custo_equip = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'equipamentos'  # Specify the correct table name

    def __str__(self):
        return self.nome_equip

class EquipmentStock(models.Model):
    id_armazem = models.IntegerField()  # Adjust field type as necessary
    id_equip = models.ForeignKey(EquipmentItem, on_delete=models.CASCADE, related_name='stocks')
    quantidade_stockequip = models.IntegerField()

    class Meta:
        db_table = 'stockequipamentos'  # Specify the correct table name
        unique_together = (('id_armazem', 'id_equip'),)  # Ensure unique combination of id_armazem and id_equip

    def __str__(self):
        return f'Stock for {self.id_equip.nome_equip}: {self.quantidade_stockequip}'