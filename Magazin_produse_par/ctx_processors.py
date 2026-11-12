from django.conf import settings
from .models import Categorie

def detalii_firma(request):
    return {"detalii_firma": settings.DETALII_FIRMA}

def meniu_categorii(request):
    categorii_cu_produse = Categorie.objects.filter(produse__isnull=False).distinct()# doar cele cu produse
    return {"categorii_meniu": categorii_cu_produse}