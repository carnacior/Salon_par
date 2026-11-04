from django.contrib import admin
from .models import Ambalaj, Categorie, Brand, Ingredient, Promotie, Produs, VariantaProdus

admin.site.site_header = "Administrare Magazin Par"
admin.site.site_title = "Admin Magazin Par"
admin.site.index_title = "Bine ai venit la panoul de administrare"

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prioritate_afisare', 'culoare')
    search_fields = ('nume',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('nume', 'tara_origine', 'an_fondare')
    search_fields = ('nume',)

@admin.register(Ambalaj)
class AmbalajAdmin(admin.ModelAdmin):
    list_display = ('nume', 'material', 'pret', 'nivel_rezistenta')
    list_filter = ('material',)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('nume', 'tip')
    list_filter = ('tip',)

@admin.register(Promotie)
class PromotieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'procent_reducere', 'data_start', 'data_final')

@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    list_display = ('nume', 'pret', 'stoc', 'categorie', 'brand', 'este_vegan')
    list_filter = ('categorie', 'brand', 'este_vegan')
    search_fields = ('nume', 'descriere')

@admin.register(VariantaProdus)
class VariantaProdusAdmin(admin.ModelAdmin):
    list_display = ('produs', 'culoare', 'volum_extra_ml', 'pret_suplimentar')