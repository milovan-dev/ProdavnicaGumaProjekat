from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'Servis&Gume_tajna_sifra'

def get_db_connection():
    konekcija = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prodavnica_guma"
    )
    return konekcija


# 1. POCETNA STRANICA
@app.route('/')
def pocetna():
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
    
    # Ovaj upit vuce tacno 4 gume za pocetnu stranicu
    upit = """
        SELECT gume.*, proizvodjaci.naziv AS proizvodjac, kategorije.naziv AS kategorija
        FROM gume
        JOIN proizvodjaci ON gume.proizvodjac_id = proizvodjaci.id
        JOIN kategorije ON gume.kategorija_id = kategorije.id
        LIMIT 4
    """
    kursor.execute(upit)
    izdvojene_gume = kursor.fetchall()
    
    kursor.close()
    konekcija.close()
    
    return render_template('index.html', gume=izdvojene_gume)

# RUTA ZA PRIKAZ GUMA NA AKCIJI
@app.route('/akcije')
def akcije():
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
    
    upit = """
        SELECT gume.*, proizvodjaci.naziv as proizvodjac, kategorije.naziv as kategorija 
        FROM gume 
        JOIN proizvodjaci ON gume.proizvodjac_id = proizvodjaci.id
        JOIN kategorije ON gume.kategorija_id = kategorije.id
        WHERE gume.popust > 0
    """
    kursor.execute(upit)
    gume_na_akciji = kursor.fetchall()
    
    kursor.close()
    konekcija.close()
    return render_template('proizvodi.html', gume=gume_na_akciji)

# GLAVNA RUTA ZA SVE PROIZVODE (sa filterima i sortiranjem)
@app.route('/proizvodi', methods=['GET'])
def proizvodi():
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
    
    upit = """
        SELECT gume.*, proizvodjaci.naziv AS proizvodjac, kategorije.naziv AS kategorija
        FROM gume
        JOIN proizvodjaci ON gume.proizvodjac_id = proizvodjaci.id
        JOIN kategorije ON gume.kategorija_id = kategorije.id
        WHERE 1=1
    """
    parametri = [] 

    sezona = request.args.get('sezona')
    kategorija = request.args.get('kategorija')
    maks_cena = request.args.get('maks_cena')
    sortiranje = request.args.get('sortiranje')
    proizvodjac = request.args.get('proizvodjac')
    sirina = request.args.get('sirina')
    visina = request.args.get('visina')
    precnik = request.args.get('precnik')

    if sezona:
        upit += " AND gume.sezona = %s"
        parametri.append(sezona)
    if kategorija:
        upit += " AND kategorije.naziv = %s"
        parametri.append(kategorija)
    if maks_cena and maks_cena != '':
        upit += " AND gume.cena <= %s"
        parametri.append(maks_cena)
    if proizvodjac:
        upit += " AND proizvodjaci.naziv = %s"
        parametri.append(proizvodjac)
    if sirina:
        upit += " AND gume.sirina = %s"
        parametri.append(sirina)
    if visina:
        upit += " AND gume.visina = %s"
        parametri.append(visina)
    if precnik:
        upit += " AND gume.precnik = %s"
        parametri.append(precnik)

    # Sortiranje po snizenoj ceni ako je na akciji
    
    if sortiranje == 'rastuce':
        upit += " ORDER BY (gume.cena * (1 - gume.popust / 100)) ASC"
    elif sortiranje == 'opadajuce':
        upit += " ORDER BY (gume.cena * (1 - gume.popust / 100)) DESC"

    kursor.execute(upit, parametri)
    sve_gume = kursor.fetchall()
    
    kursor.close()
    konekcija.close()
    
    return render_template('proizvodi.html', gume=sve_gume)


# RUTA ZA ZAKAZIVANJE SERVISA
@app.route('/zakazi', methods=['GET', 'POST'])
def zakazi_servis():
    poruka = None 
    if request.method == 'POST':
        ime_prezime = request.form.get('ime_prezime')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        vozilo = request.form.get('vozilo')
        vrsta_usluge = request.form.get('vrsta_usluge')
        datum_servisa = request.form.get('datum_servisa')

        konekcija = get_db_connection()
        kursor = konekcija.cursor()
        
        sql = """INSERT INTO zakazivanje_servisa 
                 (ime_prezime, telefon, email, vozilo, vrsta_usluge, datum_servisa) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        vrednosti = (ime_prezime, telefon, email, vozilo, vrsta_usluge, datum_servisa)
        
        kursor.execute(sql, vrednosti)
        konekcija.commit() 
        kursor.close()
        konekcija.close()
        poruka = "Vaš upit je uspešno poslat! Kontaktiraćemo vas uskoro."

    return render_template('zakazivanje.html', poruka=poruka)

# RUTA ZA DODAVANJE U KORPU (Izvrsava se u pozadini kada kliknes "Dodaj u korpu")
@app.route('/dodaj_u_korpu/<int:guma_id>', methods=['POST'])
def dodaj_u_korpu(guma_id):
    if 'korpa' not in session:
        session['korpa'] = []
    
    korpa = session['korpa']
    korpa.append(guma_id)
    session['korpa'] = korpa
    # Vraća korisnika na istu stranicu na kojoj je bio
    return redirect(request.referrer or url_for('pocetna'))

# RUTA ZA PRIKAZ SAME KORPE
@app.route('/korpa')
def pregled_korpe():
    if 'korpa' not in session or not session['korpa']:
        return render_template('korpa.html', gume_u_korpi=[], ukupno=0)
    
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
    
    # Ovaj deo formatira SQL upit u zavisnosti od toga koliko guma ima u korpi
    format_string = ','.join(['%s'] * len(session['korpa']))
    upit = f"""
        SELECT gume.*, proizvodjaci.naziv AS proizvodjac 
        FROM gume 
        JOIN proizvodjaci ON gume.proizvodjac_id = proizvodjaci.id
        WHERE gume.id IN ({format_string})
    """
    kursor.execute(upit, tuple(session['korpa']))
    gume_baza = kursor.fetchall()
    kursor.close()
    konekcija.close()
    
    gume_u_korpi = []
    ukupno = 0
    # Prolazimo kroz sve ID-jeve iz sesije i spajamo ih sa podacima iz baze
    for guma_id in session['korpa']:
        for g in gume_baza:
            if g['id'] == guma_id:
                stavka = g.copy() # Kopiramo da ne pokvarimo original
                # Racunanje tacne cene sa popustom
                prava_cena = int(float(stavka['cena']) * (1 - stavka['popust'] / 100)) if stavka.get('popust', 0) > 0 else int(float(stavka['cena']))
                stavka['prava_cena'] = prava_cena 
                
                gume_u_korpi.append(stavka)
                ukupno += prava_cena
                break
                
    return render_template('korpa.html', gume_u_korpi=gume_u_korpi, ukupno=ukupno)

# RUTA ZA PRAZNJENJE KORPE (Brise sve iz sesije)
@app.route('/isprazni_korpu')
def isprazni_korpu():
    session.pop('korpa', None)
    return redirect(url_for('pregled_korpe'))


if __name__ == '__main__':
    
    app.run(debug=True)