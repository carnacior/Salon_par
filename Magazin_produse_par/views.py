from time import time

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Ambalaj
from django.shortcuts import render  

from django.contrib import messages
from django.shortcuts import redirect

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


def index(request):
    inregistreaza(request)
    return render(request, "index.html")

def info(request):
    a = request.GET.get("data")
    aa = inregistreaza(request)
    messages.debug(request, "Modul DEBUG activ. Serverul ruleaza optim.")
    data_text = aa.get_data(a)
    return render(request, "info.html", {"data_afisata": data_text})



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

        return render(request, "log.html", {
        "sectiune_nr": sectiune_nr,
        "html_eroare": html_eroare,
        "html_lista": html_lista,
        "sectiune_statistici": sectiune_statistici,
        "sectiune_parametri": sectiune_parametri,
        })
    
def despre(request):
    inregistreaza(request)
    messages.info(request, "Afla povestea salonului nostru si al parului cu care lucram.") 
    return render(request, "despre.html")

def istoric(request):
    inregistreaza(request)
    messages.warning(request, "Atentie: Unele date din istoricul salonului sunt inca in curs de scriere.")
    return render(request, "istoric.html")  
    
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
    return render(request, 'ambalaje.html',
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
    
def produse(request):
    inregistreaza(request)
    messages.info(request, "Catalogul este in curs de actualizare. Reveniti curand!")
    return render(request, "in_lucru.html")

def contact(request):
    inregistreaza(request)
    messages.warning(request, "Timpul mediu de raspuns la programari este de 24 de ore.") 
    return render(request, "in_lucru.html")

def cos_virtual(request):
    inregistreaza(request)
    messages.error(request, "Eroare: Cosul este gol sau nu exista")
    messages.error(request, "Eroare: Nu sunteti logat")
    return render(request, "in_lucru.html")




def trimite_mesaje(request):
    messages.debug(request, "Acesta este un mesaj de depanare.")
    messages.info(request, "Acesta este un mesaj informativ.")
    messages.success(request, "Actiunea a avut succes! :D")
    messages.warning(request, "Atentie! Stocul este limitat.")
    messages.error(request, "A aparut o eroare la procesarea cererii.")
    
    return redirect('index')


