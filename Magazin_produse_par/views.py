from time import time

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Ambalaj

from django.contrib import messages
from django.shortcuts import redirect

from .models import Produs, Ingredient, Categorie

from django.shortcuts import get_object_or_404
from django.conf import settings

from django.core.mail import send_mail

from .forms import CustomUserCreationForm
from .models import Profil

from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm


ZILE = [
    "Luni", "Marti", "Miercuri", "Joi",
    "Vineri", "Sambata", "Duminica"
    ]

LUNI = [
    "",
    "Ianuarie", "Februarie", "Martie", "Aprilie",
    "Mai", "Iunie", "Iulie", "August",
    "Septembrie", "Octombrie", "Noiembrie", "Decembrie"
]
accesari = [] 
def inregistreaza(request):
    acc = Accesare(
        ip_client=request.ip,
        url=request.get_full_path(),
        parametri=request.GET.dict()
    )
    accesari.append(acc)
    print(acc)
    return acc

class Accesare:
    contor=1
    def __init__(self, ip_client, parametri={}, url=""):
        self.id= Accesare.contor
        Accesare.contor+=1
        
        self.ip_client=ip_client
        self.data= datetime.now()
        self.parametri=parametri
        self.url=url
    def __str__(self):
        return f"""
    id: {self.id}, 
    ip : {self.ip_client},
    url : {self.get_url()},
    pagina : {self.pagina()},
    data : {self.get_data()},
    parametri : {self.lista_parametri()}
    """
    def lista_parametri(self):
        rezultat = []
        for cheie, valoare in self.parametri.items():
            rezultat.append((cheie, valoare))
        return rezultat
    def get_url(self):
        return self.url
    def pagina(self):
        bucati = self.url.split("/")[2:]
        rezultat = "/" + "/".join(bucati)
        return rezultat
    def get_data(self, format=""):
        if format == "zi":
            return f"{ZILE[self.data.weekday()]}, {self.data.day} {LUNI[self.data.month]} {self.data.year}"
        elif format == "timp":
            return f"{self.data.strftime("%H:%M:%S")}"
        else:
            return f"Astazi este {ZILE[self.data.weekday()]}, {self.data.day} {LUNI[self.data.month]} {self.data.year} si este ora {self.data.strftime("%H:%M:%S")}"


def trimite_email():
    send_mail(
        subject='Salutare!',
        message='Salut. Ce mai faci?',
        html_message='<h1>Salut</h1><p>Ce mai faci?</p>',
        from_email='lucautilizator675@gmail.com',
        recipient_list=['lucautilizator675@gmail.com'],
        fail_silently=False,
    )


def index(request):
    trimite_email();
    inregistreaza(request)
    return render(request, "Magazin_produse_par/index.html")

def info(request):
    a = request.GET.get("data")
    aa = inregistreaza(request)
    messages.debug(request, "Modul DEBUG activ. Serverul ruleaza optim.")
    data_text = aa.get_data(a)
    return render(request, "Magazin_produse_par/info.html", {"data_afisata": data_text})



def valoare_coloana(a, nume):
    if nume == "id":
        return a.id
    elif nume == "ip_client":
        return a.ip_client
    elif nume == "url":
        return a.get_url()
    elif nume == "pagina":
        return a.pagina()
    elif nume == "data":
        return a.get_data()
    elif nume == "lista_parametri":
        rezultat = []
        for cheie, val in a.lista_parametri():
            rezultat.append(f"{cheie}={val}")
        return ", ".join(rezultat) if rezultat else "-"
    else:
        return ""

def calculeaza_statistici():
    numaratori = {}
    for a in accesari:
        pag = a.pagina()
        if pag in numaratori:
            numaratori[pag] += 1
        else:
            numaratori[pag] = 1

    if not numaratori:
        return None, None, 0, 0

    cea_mai_mult = max(numaratori, key=numaratori.get)
    cea_mai_putin = min(numaratori, key=numaratori.get)

    return cea_mai_putin, cea_mai_mult, numaratori[cea_mai_putin], numaratori[cea_mai_mult]

#lab 2 task 1
def log(request):
    inregistreaza(request)
    messages.debug(request, "Modul DEBUG activ. S-a accesat jurnalul de accesari al aplicatiei.")
    ultimele = request.GET.get("ultimele", None)
    m = len(accesari)

    accesari_param = request.GET.get("accesari", "")
    iduri = request.GET.getlist("iduri")
    tabel = request.GET.get("tabel", "")
    dubluri = request.GET.get("dubluri", "false")

    if accesari_param == "nr":
        sectiune_nr = f"<p><b>Numar total accesari: {m}</b></p>"
    else:
        sectiune_nr = ""

    parametri = request.GET.dict()
    nr_param = len(parametri)
    nume_param = ", ".join(parametri.keys()) if parametri else "(niciunul)"
    sectiune_parametri = f"<h3>Parametri</h3><p>{nr_param} parametri: {nume_param}</p>"

    eroare = ""
    afisate = []

    if len(iduri) > 0:
        toate = []
        for bucata in iduri:
            for x in bucata.split(","):
                toate.append(int(x))

        if dubluri == "true":
            id_final = toate
        else:
            id_final = []
            for x in toate:
                if x not in id_final:
                    id_final.append(x)

        for idc in id_final:
            for a in accesari:
                if a.id == idc:
                    afisate.append(a)
                    break

    elif ultimele is None or ultimele == "":
        afisate = accesari

    else:
        try:
            n = int(ultimele)
        except ValueError:
            eroare = "Parametrul nu este in format corect."
            afisate = []
        else:
            if n > m:
                afisate = accesari
                eroare = f"Exista doar {m} accesari fata de {n} accesari cerute"
            else:
                afisate = accesari[-n:]

    if tabel == "tot":
        coloane = ["id", "ip_client", "url", "pagina", "data", "lista_parametri"]
    elif tabel != "":
        coloane = tabel.split(",")
    else:
        coloane = []

#html
    if coloane:
        html_tabel = "<table border='1' cellpadding='5'>"
        html_tabel += "<tr>"
        for c in coloane:
            html_tabel += f"<th>{c}</th>"
        html_tabel += "</tr>"
        for a in afisate:
            html_tabel += "<tr>"
            for c in coloane:
                html_tabel += f"<td>{valoare_coloana(a, c)}</td>"
            html_tabel += "</tr>"
        html_tabel += "</table>"
        html_lista = html_tabel

    elif accesari_param == "detalii":
        linii = []
        for a in afisate:
            linii.append(f"<li>{a.get_data()}</li>")
        if linii:
            html_lista = "<ul>" + "".join(linii) + "</ul>"
        else:
            html_lista = "<p>Nu exista accesari.</p>"

    else:
        if afisate:
            parti = []
            for a in afisate:
                parti.append(str(a).replace("\n", "<br>"))
            html_lista = "<br><br>".join(parti)
        else:
            html_lista = "<p>Nu exista accesari.</p>"

    if eroare:
        html_eroare = f"<p style='color:red'>{eroare}</p>"
    else:
        html_eroare = ""

    cea_mai_putin, cea_mai_mult, nr_min, nr_max = calculeaza_statistici()

    if cea_mai_mult is None:
        sectiune_statistici = ""
    else:
        sectiune_statistici = f"""
        <h3>Statistici</h3>
        <p>Cea mai accesata pagina: <b>{cea_mai_mult}</b> ({nr_max} accesari)</p>
        <p>Cea mai putin accesata pagina: <b>{cea_mai_putin}</b> ({nr_min} accesari)</p>
        """

    return render(request, "Magazin_produse_par/log.html", {
    "sectiune_nr": sectiune_nr,
    "html_eroare": html_eroare,
    "html_lista": html_lista,
    "sectiune_statistici": sectiune_statistici,
    "sectiune_parametri": sectiune_parametri,
    })
    
def despre(request):
    inregistreaza(request)
    messages.info(request, "Afla povestea salonului nostru si al parului cu care lucram.") 
    return render(request, "Magazin_produse_par/despre.html")

def istoric(request):
    inregistreaza(request)
    messages.warning(request, "Atentie: Unele date din istoricul salonului sunt inca in curs de scriere.")
    return render(request, "Magazin_produse_par/istoric.html")  
    
def afisare_ambalaje(request):
    nrPagina=request.GET.get("pagina", 1)
    # veti trata situatia in care nu e dat un numar intreg
    ambalaje=Ambalaj.objects.all()
    paginator = Paginator(ambalaje, 5)
    mesajEroare=None
    try:
        obPagina = paginator.page(nrPagina)
    except EmptyPage:
        obPagina=None
        mesajEroare = "Nu mai sunt ambalaje"
    return render(request, 'Magazin_produse_par/ambalaje.html',
                    {
                        'pagina': obPagina,
                        'eroare': mesajEroare
                    }
    )



def detalii_accesare(request, id):
    inregistreaza(request)

    for a in accesari:
        if a.id == int(id):
            return HttpResponse(f"""
                <html><body>
                    <h1>Accesare #{a.id}</h1>
                    <pre>{str(a).replace(chr(10), '<br>')}</pre>
                </body></html>""")

    return HttpResponse(f"""
        <html><body>
            <h1>Nu exista accesarea cu id-ul {id}</h1>
        </body></html>""")
    
def _prelucreaza_produse(request, queryset_initial):
    # sortare
    sort_param = request.GET.get('sort', 'a')
    col_param = request.GET.get('col', 'pret')
    if sort_param == 'd':
        queryset_initial = queryset_initial.order_by(f'-{col_param}')
    else:
        queryset_initial = queryset_initial.order_by(col_param)

    # filtrare
    taguri_active = request.GET.getlist('tag')
    if taguri_active:
        for tag_text in taguri_active:
            queryset_initial = queryset_initial.filter(taguri__contains=[tag_text])

    toate_tagurile = set()
    for p in Produs.objects.all():
        if p.taguri:
            toate_tagurile.update(p.taguri)

    # paginarea
    paginator = Paginator(queryset_initial, settings.PROD_PER_PAG)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return {
        'page_obj': page_obj,
        'toate_tagurile': list(toate_tagurile),
        'taguri_active': taguri_active,
        'sort_curent': sort_param,
        'col_curenta': col_param,
        'STOC_MIN': settings.STOC_MIN,
    }

def produse(request):
    inregistreaza(request)
    context = _prelucreaza_produse(request, Produs.objects.all())
    return render(request, "Magazin_produse_par/produse.html", context)

def categorie_produse(request, slug):
    inregistreaza(request)
    categorie_curenta = get_object_or_404(Categorie, nume__iexact=slug.replace('-', ' '))
    produse_categorie = Produs.objects.filter(categorie=categorie_curenta)
    
    context = _prelucreaza_produse(request, produse_categorie)
    context['categorie_curenta'] = categorie_curenta
    
    return render(request, "Magazin_produse_par/produse.html", context)

def contact(request):
    inregistreaza(request)
    messages.warning(request, "Timpul mediu de raspuns la programari este de 24 de ore.") 
    return render(request, "Magazin_produse_par/in_lucru.html")

def cos_virtual(request):
    inregistreaza(request)
    messages.error(request, "Eroare: Cosul este gol sau nu exista")
    messages.error(request, "Eroare: Nu sunteti logat")
    return render(request, "Magazin_produse_par/in_lucru.html")




def trimite_mesaje(request):
    messages.debug(request, "Acesta este un mesaj de depanare.")
    messages.info(request, "Acesta este un mesaj informativ.")
    messages.success(request, "Actiunea a avut succes! :D")
    messages.warning(request, "Atentie! Stocul este limitat.")
    messages.error(request, "A aparut o eroare la procesarea cererii.")
    
    return redirect('index')

def detalii_produs(request, slug):
    inregistreaza(request)
    
    #cautam dupa slug, daca nu exista ne da 404
    produs = get_object_or_404(Produs, slug=slug)
    
    #luam din aceeasi categorie, excluzand produsul curent si le amestecam aleatoriu
    produse_similare = Produs.objects.filter(categorie=produs.categorie).exclude(id=produs.id).order_by('?')[:settings.K_PRODUSE_SIMILARE]
    
    return render(request, "Magazin_produse_par/produs_detalii.html", {
        "produs": produs,
        "produse_similare": produse_similare,
        'STOC_MIN': settings.STOC_MIN,
    })

####################lab6

def inregistrare(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            strada = form.cleaned_data.get('strada')
            data_nasterii = form.cleaned_data.get('data_nasterii')
            bio = form.cleaned_data.get('bio')
            
            if strada or data_nasterii or bio:
                # daca a completat ceva, cream profilul
                Profil.objects.create(
                    user=user,
                    strada=strada,
                    data_nasterii=data_nasterii,
                    bio=bio
                )
            
            messages.success(request, "Contul a fost creat cu succes! Te poti loga.")
            return redirect('login') # trimite la login dupa inregistrare
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'Magazin_produse_par/inregistrare.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if form.cleaned_data.get('tine_minte'):
                request.session.set_expiry(86400)#secunde
            else:
                request.session.set_expiry(0)
                
            messages.success(request, f"Bine ai revenit, {user.username}!")
            return redirect('profil')
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'Magazin_produse_par/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Te-ai delogat cu succes.")
    return redirect('index')

def profil(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        profil_user = Profil.objects.get(user=request.user)
    except Profil.DoesNotExist:
        profil_user = None
        
    request.session['ultima_vizita_profil'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    ultima_vizita = request.session.get('ultima_vizita_profil')
    
    return render(request, 'Magazin_produse_par/profil.html', {
        'profil_user': profil_user,
        'ultima_vizita': ultima_vizita
    })
    
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def schimba_parola(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) #tine logat dupa schimbare
            messages.success(request, "Parola a fost schimbata cu succes!")
            return redirect('profil')
        else:
            messages.error(request, "Te rugam sa corectezi erorile de mai jos.")
    else:
        form = PasswordChangeForm(user=request.user)
        
    return render(request, 'Magazin_produse_par/schimba_parola.html', {'form': form})



from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, ProfilUpdateForm


def editeaza_profil(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    profil_user, created = Profil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilUpdateForm(request.POST, instance=profil_user)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Datele au fost actualizate cu succes!")
            return redirect('profil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilUpdateForm(instance=profil_user)
        
    return render(request, 'Magazin_produse_par/editeaza_profil.html', {
        'u_form': u_form,
        'p_form': p_form
    })