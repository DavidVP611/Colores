from django.db import models

# Create your models here.
class Colors_Inventory(models.Model):
    code = models.IntegerField('Código', primary_key = True)
    name = models.CharField('Color', max_length = 200)
    quantity = models.IntegerField('Cantidad', default=0)
    
    class Meta:
        verbose_name = "Inventario del color"
        verbose_name_plural = "Inventario de colores"
    def __str__(self):
        return f"{self.code}. {self.name} - N° {self.quantity}"