from django.db import models

class acesso_pgestao(models.Model):
    id_utilpgestao = models.IntegerField(primary_key=True)
    password_pgestao = models.CharField(max_length=50)
    id_nivel = models.IntegerField(choices=[(1, 'Nível 1'), (2, 'Nível 2')], default=2)

    class Meta:
        db_table = 'acesso_pgestao'
