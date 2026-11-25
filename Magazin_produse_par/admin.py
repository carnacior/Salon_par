from django.contrib import admin
from django.utils.html import format_html
import csv
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
from .models import (
    Ambalaj, Categorie, Brand, Ingredient, Promotie, Produs, VariantaProdus,
    CustomUser, Profil, Comanda, ComandaProdus, Angajat, Departament, 
    Review, Voucher, UtilizatorVoucher, ListaFavorite, ListaFavoriteProdus
)

#8
admin.site.site_header = "Administrare Magazin Par"
admin.site.site_title = "Admin Magazin Par"
admin.site.index_title = "Bine ai venit la panoul de administrare"
admin.site.site_url = 'http://127.0.0.1:8000/Magazin_produse_par/' 


#10 - actiunile
@admin.action(description="Exporta produsele selectate in format CSV")
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produse_exportate.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nume', 'Pret', 'Stoc', 'Categorie', 'Brand'])
    for produs in queryset:
        writer.writerow([produs.nume, produs.pret, produs.stoc, produs.categorie.nume, produs.brand.nume])
    return response

@admin.action(description="Marcheaza produsele selectate ca fiind Vegane")
def marcheaza_vegan(modeladmin, request, queryset):
    queryset.update(este_vegan=True)


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'prioritate_afisare', 'culoare', 'numar_produse')
    search_fields = ('nume', 'descriere')
    search_help_text = "Cautati dupa numele sau descrierea categoriei."
    list_filter = ('prioritate_afisare',)

    #functie one to many
    @admin.display(description="Nr. Produse")
    def numar_produse(self, obj):
        return obj.produse.count()


@admin.register(Produs)
class ProdusAdmin(admin.ModelAdmin):
    # 6
    list_per_page = 5
    
    #4 ordonam descrescator dupa pret
    ordering = ('-pret',)
    
    # 5
    list_filter = ('categorie', 'brand', 'este_vegan')
    
    #3 - se regaseste la toate modelele
    search_fields = ('nume', 'descriere', 'taguri')
    search_help_text = "Puteti cauta produsele dupa nume sau cuvinte din descriere."
    
    #10
    actions = [export_csv, marcheaza_vegan]

    #1
    list_display = ('nume', 'pret_formatat', 'stoc', 'categorie', 'brand')
    
    @admin.display(description="Pret (RON)", ordering='pret')
    def pret_formatat(self, obj):
        #2, formatez pretul  si ii adaug descriere implicita + ordonare( sa fie functionabila in continuare )
        return format_html(
            '<b style="color: green; font-style: italic;">{} RON</b>',
            obj.pret
        )
        
    @admin.display(description="Tag-uri")
    def afiseaza_taguri(self, obj):
        if obj.taguri:
            return ", ".join(obj.taguri)
        return "-"

    #7
    fieldsets = (
        ('Informatii Principale', {
            'fields': ('nume', 'slug', 'categorie', 'brand', 'pret', 'stoc')
        }),
        ('Informatii Optionale (Click pentru a extinde)', { # pot fi null, blank sau optionale
            'classes': ('collapse',), # sa fie colapsabil
            'fields': ('descriere', 'volum_ml', 'data_expirare', 'este_vegan', 'lista_beneficii', 'taguri', 'imagine', 'ambalaj', 'ingrediente', 'promotii'),
        }),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('nume', 'tara_origine', 'an_fondare')
    search_fields = ('nume', 'tara_origine')
    search_help_text = "Cautati dupa numele brandului sau tara de origine."

@admin.register(Ambalaj)
class AmbalajAdmin(admin.ModelAdmin):
    list_display = ('nume', 'material', 'pret', 'nivel_rezistenta')
    list_filter = ('material',)
    search_fields = ('nume', 'descriere')
    search_help_text = "Cautati dupa numele ambalajului."

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('nume', 'tip')
    list_filter = ('tip',)
    search_fields = ('nume', 'descriere')
    search_help_text = "Cautati dupa numele ingredientului."

@admin.register(Promotie)
class PromotieAdmin(admin.ModelAdmin):
    list_display = ('nume', 'procent_reducere', 'data_start', 'data_final')
    search_fields = ('nume',)
    search_help_text = "Cautati promotia dupa nume."

@admin.register(VariantaProdus)
class VariantaProdusAdmin(admin.ModelAdmin):
    list_display = ('produs', 'culoare', 'volum_extra_ml')
    search_fields = ('produs__nume', 'culoare')
    search_help_text = "Cautati varianta dupa numele produsului parinte sau culoare."
############################    
class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name = "Detalii Profil"

class CustomUserAdmin(UserAdmin):
    inlines = (ProfilInline,)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informatii Suplimentare', {'fields': ('telefon', 'tara', 'judet')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'strada', 'data_nasterii')
    search_fields = ('user__username', 'strada')


    
#########


@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilizator', 'data_inregistrarii', 'status', 'prin_curier')
    list_filter = ('status', 'prin_curier', 'data_inregistrarii')
    search_fields = ('utilizator__username', 'id')

@admin.register(ComandaProdus)
class ComandaProdusAdmin(admin.ModelAdmin):
    list_display = ('comanda', 'produs', 'cantitate')
    search_fields = ('comanda__id', 'produs__nume')

@admin.register(Angajat)
class AngajatAdmin(admin.ModelAdmin):
    list_display = ('user', 'salariu', 'data_angajarii')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    list_display = ('nume', 'sef')
    search_fields = ('nume',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('produs', 'utilizator', 'nota', 'data')
    list_filter = ('nota', 'data')
    search_fields = ('produs__nume', 'utilizator__username', 'comentariu')

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('cod', 'procent_reducere')
    search_fields = ('cod',)

@admin.register(UtilizatorVoucher)
class UtilizatorVoucherAdmin(admin.ModelAdmin):
    list_display = ('utilizator', 'voucher', 'data_acordarii')
    search_fields = ('utilizator__username', 'voucher__cod')

@admin.register(ListaFavorite)
class ListaFavoriteAdmin(admin.ModelAdmin):
    list_display = ('nume_lista', 'utilizator')
    search_fields = ('nume_lista', 'utilizator__username')

@admin.register(ListaFavoriteProdus)
class ListaFavoriteProdusAdmin(admin.ModelAdmin):
    list_display = ('lista_favorite', 'produs')
    search_fields = ('lista_favorite__nume_lista', 'produs__nume')