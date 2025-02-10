from djongo import models

class User(models.Model):
    #_id = models.ObjectIdField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    nome = models.CharField(max_length=100)
    nif = models.CharField(max_length=20)
    telemovel = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    morada = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        # Ensure email is lowercase before saving
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
    

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
    

