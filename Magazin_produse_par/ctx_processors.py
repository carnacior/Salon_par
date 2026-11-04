from django.conf import settings

def detalii_firma(request):
    return {"detalii_firma": settings.DETALII_FIRMA}