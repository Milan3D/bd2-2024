from djongo import models

class User(models.Model):
    _id = models.ObjectIdField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    nome = models.CharField(max_length=100)
    nif = models.CharField(max_length=9)
    telemovel = models.CharField(max_length=9)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=100)


    class Meta:
        db_table = 'USERS'

    def __str__(self):
        return self.username
    

class Equipment(models.Model):
    nome_equip_pgsidcampo = models.CharField(max_length=100)
    desc_equip_pgsidcampo = models.TextField()
    custo_equip_pgsidcampo = models.DecimalField(max_digits=10, decimal_places=2)
    foto_url = models.URLField()

    class Meta:
        db_table = 'EQUIPAMENTOS'

    def __str__(self):
        return self.nome_equip_pgsidcampo
    


class Purchase(models.Model):
    username = models.CharField(max_length=100)
    produto = models.CharField(max_length=100)
    total = models.IntegerField()
    timestamp = models.CharField(max_length=100)

    class Meta:
        db_table = 'COMPRAS'

    def __str__(self):
        return f"Compra de {self.username} em {self.timestamp}"
    

