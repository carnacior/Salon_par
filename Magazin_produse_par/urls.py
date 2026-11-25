from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('info', views.info, name="info"),
    path('log', views.log, name="log"),
    path('istoric', views.istoric, name="istoric"),
    path('despre', views.despre, name="despre"),
    path("ambalaje", views.afisare_ambalaje, name="afisare_ambalaje"),
    
    re_path(r'^accesare(?P<id>\d+)$', views.detalii_accesare, name="detalii_accesare"),
    
    path('produse', views.produse, name="produse"),
    path('contact', views.contact, name="contact"),
    path('cos_virtual', views.cos_virtual, name="cos_virtual"),
    path('trimite_mesaje', views.trimite_mesaje, name="trimite_mesaje"),
    path('produs/<slug:slug>/', views.detalii_produs, name="detalii_produs"),
    path('categorii/<slug:slug>/', views.categorie_produse, name="categorie_produse"),
    
    path('inregistrare/', views.inregistrare, name="inregistrare"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profil/', views.profil, name="profil"),
    
    path('schimba-parola/', views.schimba_parola, name="schimba_parola"),
    path('editeaza-profil/', views.editeaza_profil, name="editeaza_profil"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)