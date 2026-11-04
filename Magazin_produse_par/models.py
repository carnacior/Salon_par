from django.db import models


class Ambalaj(models.Model):
    class MaterialChoices(models.TextChoices):
        PLASTIC = 'plastic', 'Plastic'
        HARTIE = 'hartie', 'Hartie'
        CARTON = 'carton', 'Carton'
        ALUMINIU = 'aluminiu', 'Aluminiu'

    class Meta:
        verbose_name_plural = "Ambalaje"
        ordering = ['nume']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(nivel_rezistenta__lte=10) & models.Q(nivel_rezistenta__gte=1),
                name='limite_rezista_ambalaj',
                violation_error_message="Nivelul de rezistenta trebuie sa fie intre 1 si 10 inclusiv!"
            )
        ]
        indexes = [
            models.Index(fields=['nume'], name='ambalaj_nume_idx'),
        ]

    nume = models.CharField(
        max_length=200,
        unique=True,
        help_text="Numele comercial al ambalajului",
        error_messages={
            'unique': "Un ambalaj cu acest nume exista deja.",
            'blank': "Numele nu poate fi gol.",
            'max_length': "Numele poate avea maxim 200 caractere.",
        }
    )
    culoare = models.CharField(max_length=100, null=True)
    nivel_rezistenta = models.PositiveIntegerField(
        help_text="Valori intre 1 si 10. Un numar mai mare indica rezistenta mai mare",
        null=True
    )
    descriere = models.TextField(null=True)
    material = models.CharField(
        max_length=10,
        choices=MaterialChoices.choices,
        default=MaterialChoices.PLASTIC,
        help_text="Materialul din care e confectionat ambalajul"
    )
    pret = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00,
        error_messages={
            'invalid': "Introduceti un pret valid (ex: 12.50).",
            'max_digits': "Pretul poate avea maxim 5 cifre.",
        }
    )

    def __str__(self):
        return f"{self.nume}: {self.culoare}"


class Categorie(models.Model):
    class Meta:
        verbose_name_plural = "Categorii"
        ordering = ['-prioritate_afisare', 'nume']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(prioritate_afisare__gte=0),
                name='prioritate_categorie_pozitiva',
                violation_error_message="Prioritatea trebuie sa fie >= 0."
            )
        ]
        indexes = [
            models.Index(fields=['nume'], name='categorie_nume_idx'),
        ]

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            'unique': "O categorie cu acest nume exista deja.",
            'blank': "Numele categoriei nu poate fi gol.",
        }
    )
    descriere = models.TextField(null=True)
    culoare = models.CharField(
        max_length=7,
        default='#FFFFFF',
        blank=True,
        help_text="Cod hex pentru culoarea reprezentativa"
    )
    sigla = models.CharField(
        max_length=50,
        default='fa-box',
        help_text="Numele iconului FontAwesome sau calea catre imagine"
    )
    prioritate_afisare = models.PositiveIntegerField(
        default=0,
        help_text="Prioritate mai mare = apare mai sus in meniu"
    )

    def __str__(self):
        return self.nume


class Brand(models.Model):
    class Meta:
        verbose_name_plural = "Branduri"
        ordering = ['nume']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(an_fondare__gte=1800),
                name='an_fondare_valid',
                violation_error_message="Anul fondarii trebuie sa fie >= 1800."
            )
        ]
        indexes = [
            models.Index(fields=['nume'], name='brand_nume_idx'),
        ]

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={
            'unique': "Un brand cu acest nume exista deja.",
            'blank': "Numele brandului nu poate fi gol.",
        }
    )
    tara_origine = models.CharField(max_length=100, null=True)
    an_fondare = models.IntegerField(null=True)
    email_contact = models.EmailField(
        error_messages={
            'invalid': "Introduceti o adresa de email valida.",
        }
    )
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nume


class Ingredient(models.Model):
    class TipChoices(models.TextChoices):
        NATURAL = 'natural', 'Natural'
        CHIMIC = 'chimic', 'Chimic'
        SINTETIC = 'sintetic', 'Sintetic'

    class Meta:
        verbose_name_plural = "Ingrediente"

    nume = models.CharField(
        max_length=100,
        unique=True,
        help_text="Numele ingredientului (ex: argan, keratina)"
    )
    tip = models.CharField(
        max_length=10,
        choices=TipChoices.choices,
        default=TipChoices.NATURAL,
        help_text="Categoria din care face parte ingredientul"
    )
    descriere = models.TextField(null=True)

    def __str__(self):
        return f"{self.nume} ({self.tip})"


class Promotie(models.Model):
    class Meta:
        verbose_name_plural = "Promotii"
        ordering = ['-data_start']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(procent_reducere__gte=1) & models.Q(procent_reducere__lte=100),
                name='procent_reducere_valid',
                violation_error_message="Procentul de reducere trebuie sa fie intre 1 si 100."
            ),
            models.CheckConstraint(
                condition=models.Q(data_final__gt=models.F('data_start')),
                name='data_final_dupa_start',
                violation_error_message="Data de final trebuie sa fie dupa data de start."
            )
        ]

    nume = models.CharField(
        max_length=200,
        unique=True,
        error_messages={
            'unique': "O promotie cu acest nume exista deja.",
        }
    )
    procent_reducere = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Procentul intre 1 si 100"
    )
    data_start = models.DateField()
    data_final = models.DateField()

    def __str__(self):
        return f"{self.nume} ({self.procent_reducere}%)"


class Produs(models.Model):
    class Meta:
        verbose_name_plural = "Produse"
        ordering = ['nume']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret__gt=0),
                name='pret_produs_pozitiv',
                violation_error_message="Pretul trebuie sa fie > 0."
            ),
            models.CheckConstraint(
                condition=models.Q(stoc__gte=0),
                name='stoc_produs_pozitiv',
                violation_error_message="Stocul trebuie sa fie >= 0."
            )
        ]
        indexes = [
            models.Index(fields=['nume'], name='produs_nume_idx'),
            models.Index(fields=['pret'], name='produs_pret_idx'),
        ]

    nume = models.CharField(
        max_length=200,
        unique=True,
        help_text="Numele complet al produsului",
        error_messages={
            'unique': "Un produs cu acest nume exista deja.",
            'max_length': "Numele poate avea maxim 200 caractere.",
            'blank': "Numele nu poate fi gol.",
        }
    )
    slug = models.SlugField(unique=True)
    descriere = models.TextField(null=True)
    pret = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        error_messages={
            'invalid': "Introduceti un pret valid.",
            'max_digits': "Pretul poate avea maxim 8 cifre.",
        }
    )
    stoc = models.PositiveIntegerField(
        help_text="Cantitatea disponibila in stoc"
    )
    volum_ml = models.PositiveIntegerField(
        help_text="Volumul in mililitri"
    )
    data_expirare = models.DateField(null=True)
    este_vegan = models.BooleanField(default=False)
    lista_beneficii = models.JSONField(
        default=list,
        help_text="Lista de beneficii (ex: ['hidratare', 'luciu'])"
    )
    imagine = models.ImageField(upload_to='produse/', null=True, blank=True)
    data_adaugare = models.DateTimeField(auto_now_add=True)

    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produse')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='produse')
    ambalaj = models.ForeignKey(Ambalaj, on_delete=models.SET_NULL, null=True, related_name='produse')
    ingrediente = models.ManyToManyField(Ingredient, related_name='produse')
    promotii = models.ManyToManyField(Promotie, related_name='produse', blank=True)

    def __str__(self):
        return self.nume


class VariantaProdus(models.Model):
    class Meta:
        verbose_name_plural = "Variante produse"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(pret_suplimentar__gte=0),
                name='pret_suplimentar_pozitiv',
                violation_error_message="Pretul suplimentar trebuie sa fie >= 0."
            )
        ]

    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='variante')
    culoare = models.CharField(max_length=50)
    volum_extra_ml = models.PositiveIntegerField(default=0)
    pret_suplimentar = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.produs.nume} - {self.culoare}"