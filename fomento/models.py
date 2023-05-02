from django.db import models
from account.models import Account
from django.utils import timezone


class AuditModel(models.Model):
    # created_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True,
    #                                related_name='audit_created_by')
    # updated_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True,
    #                                related_name='updated_created_by')
    created_at = models.DateTimeField("Creación del Registro:", auto_now_add=True)
    updated_at = models.DateTimeField("Modificación del Registro:", auto_now=True)

    class Meta:
        abstract = True


class FomentoFile(AuditModel):
    filename = models.CharField("Archivo origen", max_length=100)
    year = models.CharField("Año", max_length=4)
    month = models.CharField("Mes", max_length=2)
    processed = models.BooleanField('Procesado', default=False)
    reprocessed = models.BooleanField('Procesado', default=False)


class Fomento(AuditModel):
    """
        Model Fomento
        Fields:
            fomento
            year
            month
            day
            file

    """
    fomento = models.DecimalField(max_digits=10, decimal_places=2)
    file = models.ForeignKey(FomentoFile, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Archivo")
    year = models.CharField("Año", max_length=4)
    month = models.CharField("Mes", max_length=2)
    day = models.CharField("Día", max_length=2)

    def __str__(self):
        return self.fomento


class FomentoTmp(AuditModel):
    """
        Model FomentoTemp
        Fields:
            fomento
            file

    """
    fomento = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.CharField("Año", max_length=4)
    month = models.CharField("Mes", max_length=2)
    day = models.CharField("Día", max_length=2)
