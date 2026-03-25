from collections import Counter
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
from werkzeug.security import generate_password_hash, check_password_hash 
import mysql.connector

app = Flask(__name__)
app.secret_key = 'kemoimpex_tajna_sifra'

def get_db_connection():
    konekcija = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prodavnica_guma"
    )
    return konekcija

# Pocetna stranica
@app.route('/')
def pocetna():
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
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



# Login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        konekcija = get_db_connection()
        kursor = konekcija.cursor(dictionary=True)
        

        email = request.form['email']
        lozinka = request.form['lozinka']

        kursor.execute("SELECT * FROM korisnici_login_info WHERE email = %s", (email,))
        korisnik = kursor.fetchone()

        if korisnik and check_password_hash(korisnik['lozinka'], lozinka):
            session['korisnik_id'] = korisnik['id']
            session['uloga'] = korisnik['uloga']
            
            if korisnik['sacuvana_korpa']:
                session['korpa'] = json.loads(korisnik['sacuvana_korpa'])
            
            kursor.close() 
            konekcija.close() 
            return redirect('/')
        else:
            kursor.close() 
            konekcija.close() 
            return render_template('login.html', greska="Pogrešan e-mail ili lozinka!")

    return render_template('login.html')

@app.route('/logout')
def logout():
    
    if 'korisnik_id' in session and 'korpa' in session:
        konekcija = get_db_connection()
        kursor = konekcija.cursor()
        
        korpa_json = json.dumps(session['korpa']) 
        
        kursor.execute("UPDATE korisnici_login_info SET sacuvana_korpa = %s WHERE id = %s", 
                       (korpa_json, session['korisnik_id']))
        konekcija.commit()
        kursor.close()
        konekcija.close()

    session.clear() 
    return redirect('/')


# Register

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        konekcija = get_db_connection()
        kursor = konekcija.cursor(dictionary=True)

        ime = request.form['ime']
        email = request.form['email']
        lozinka = request.form['lozinka']

        kursor.execute("SELECT * FROM korisnici_login_info WHERE email = %s", (email,))
        postojeci_korisnik = kursor.fetchone()

        if postojeci_korisnik:
            return render_template('register.html', greska="Ovaj e-mail je već registrovan!")

        kriptovana_lozinka = generate_password_hash(lozinka)

        kursor.execute("""
            INSERT INTO korisnici_login_info (ime, email, lozinka, uloga) 
            VALUES (%s, %s, %s, 'korisnik')
        """, (ime, email, kriptovana_lozinka))
        konekcija.commit()

        kursor.close()

        return redirect('/login')

    return render_template('register.html')

# Proizvodi
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
    if maks_cena:
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

    if sortiranje == 'rastuce':
        upit += " ORDER BY (gume.cena * (1 - gume.popust / 100)) ASC"
    elif sortiranje == 'opadajuce':
        upit += " ORDER BY (gume.cena * (1 - gume.popust / 100)) DESC"

    kursor.execute(upit, parametri)
    sve_gume = kursor.fetchall()
    kursor.close()
    konekcija.close()
    return render_template('proizvodi.html', gume=sve_gume)

# Kontakt stranica
@app.route('/kontakt')
def kontakt_strana():
    return render_template('/kontakt.html')

# Zakazivanje
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

# Dodavanje u korpu
@app.route('/dodaj_u_korpu/<int:guma_id>', methods=['POST'])
def dodaj_u_korpu(guma_id):
    if 'korpa' not in session:
        session['korpa'] = []
    
    korpa = session['korpa']
    korpa.append(guma_id)
    session['korpa'] = korpa
    session.modified = True 

    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(uspeh=True, broj_u_korpi=len(korpa))
    
    
    return redirect(request.referrer or url_for('pocetna'))

# Korpa
@app.route('/korpa')
def pregled_korpe():
    if 'korpa' not in session or not session['korpa']:
        return render_template('korpa.html', gume_u_korpi=[], ukupno=0)
    
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
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
    for guma_id in session['korpa']:
        for g in gume_baza:
            if g['id'] == guma_id:
                stavka = g.copy()
                prava_cena = int(float(stavka['cena']) * (1 - stavka['popust'] / 100)) if stavka.get('popust', 0) > 0 else int(float(stavka['cena']))
                stavka['prava_cena'] = prava_cena
                gume_u_korpi.append(stavka)
                ukupno += prava_cena
                break
    return render_template('korpa.html', gume_u_korpi=gume_u_korpi, ukupno=ukupno)


# Praznjenje korpe
@app.route('/isprazni_korpu')
def isprazni_korpu():
    session['korpa'] = [] 
    session.modified = True 
    return redirect(url_for('pregled_korpe'))

# Checkout
@app.route('/checkout')
def checkout():
    
    if 'korpa' not in session or not session['korpa']:
        return redirect(url_for('pregled_korpe'))
    
    try:
        konekcija = get_db_connection()
        kursor = konekcija.cursor(dictionary=True)
        
        
        format_string = ','.join(['%s'] * len(session['korpa']))
        kursor.execute(f"SELECT id, cena, popust FROM gume WHERE id IN ({format_string})", tuple(session['korpa']))
        gume_baza = kursor.fetchall()
        
        
        ukupno = 0
        for guma_id in session['korpa']:
            for g in gume_baza:
                if g['id'] == guma_id:
                    prava_cena = int(float(g['cena']) * (1 - g['popust'] / 100)) if g.get('popust', 0) > 0 else int(float(g['cena']))
                    ukupno += prava_cena
                    break
                    
        kursor.close()
        konekcija.close()
        
        
        return render_template('checkout.html', ukupno=ukupno)
        
    except Exception as e:
        print(f"Greška u checkout-u: {e}")
        return "Došlo je do greške prilikom obrade porudžbine. Proverite bazu podataka."
    

 # Kupovina   
@app.route('/kupi', methods=['POST'])
def kupi():
    ime_prezime = request.form.get('ime_prezime')
    adresa = request.form.get('adresa')
    telefon = request.form.get('telefon')
    ukupna_cena = request.form.get('ukupna_cena')

    if 'korpa' not in session or not session['korpa']:
        return "Korpa je prazna!", 400

    konekcija = get_db_connection()
    kursor = konekcija.cursor()

    try:
        # Ubacivanje u tabelu porudzbine
        sql_porudzbina = """
            INSERT INTO porudzbine (ime_prezime, adresa, telefon, ukupna_cena)
            VALUES (%s, %s, %s, %s)
        """
        kursor.execute(sql_porudzbina, (ime_prezime, adresa, telefon, ukupna_cena))
        porudzbina_id = kursor.lastrowid

        
        format_string = ','.join(['%s'] * len(session['korpa']))
        
        kursor.execute(f"SELECT id, cena, popust, model FROM gume WHERE id IN ({format_string})", tuple(session['korpa']))
        gume_baza = kursor.fetchall()

        
        for guma_id in session['korpa']:
            for g in gume_baza:
                if g[0] == guma_id:  
                    prava_cena = float(g[1]) * (1 - g[2] / 100) if g[2] > 0 else float(g[1])
                    naziv_gume = g[3] 
                    
                    sql_stavka = """
                        INSERT INTO stavke_porudzbine (porudzbina_id, guma_id, naziv_gume, kolicina, cena_po_komadu)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    kursor.execute(sql_stavka, (porudzbina_id, guma_id, naziv_gume, 1, prava_cena))
                    break

        konekcija.commit()
        session.pop('korpa', None)
        session.modified = True

        slika_putanja = url_for('static', filename='images/hero-pozadina.jpg')
        return f"""
        <div style="font-family: sans-serif; text-align: center; padding: 50px; color: white; 
                    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('{slika_putanja}');
                    background-size: cover; background-position: center; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h1 style="color: #27ae60; font-size: 3rem;">✅ Uspešno ste poručili!</h1>
            <p style="font-size: 1.5rem;">Hvala na poverenju. Vaša porudžbina je uspešno evidentirana.</p>
            <br>
            <a href="/" style="text-decoration: none; background: #3498db; color: white; padding: 15px 30px; 
                               border-radius: 5px; font-weight: bold; font-size: 1.2rem;">
                Vrati se na početnu
            </a>
        </div>
        """

    except Exception as e:
        konekcija.rollback()
        print(f"Greška pri kupovini: {e}")
        return f"Došlo je do greške: {e}", 500

    finally:
        kursor.close()
        konekcija.close()

#stavke porudzbina
@app.route('/kreiraj_tabelu_stavke')
def kreiraj_tabelu_stavke():
    konekcija = get_db_connection()
    kursor = konekcija.cursor()
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS porudzbine_stavke (
            id INT(11) NOT NULL AUTO_INCREMENT,
            porudzbina_id INT(11) NOT NULL,
            guma_id INT(11) NOT NULL,
            naziv_gume VARCHAR(255) NOT NULL, -- OVO JE NOVA KOLONA
            kolicina INT(11) NOT NULL DEFAULT 1,
            cena_komad DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (id),
            INDEX (porudzbina_id),
            INDEX (guma_id),
            CONSTRAINT fk_porudzbina FOREIGN KEY (porudzbina_id) 
                REFERENCES porudzbine(id) ON DELETE CASCADE,
            CONSTRAINT fk_guma FOREIGN KEY (guma_id) 
                REFERENCES gume(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        kursor.execute(sql)
        konekcija.commit()
        return "Tabela porudzbine_stavke je uspesno kreirana ili vec postoji!" 
    except Exception as e:
        konekcija.rollback()
        return f"Greska pri kreiranju tabele: {e}"
    finally:
        kursor.close()
        konekcija.close()


# RUTA ZA PRIKAZ SAMO GUMA KOJE SU NA AKCIJI
@app.route('/akcije')
def akcije():
    konekcija = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prodavnica_guma"
    )
    kursor = konekcija.cursor(dictionary=True)
    
    # Biramo samo one gume koje imaju definisan popust
    upit = """
        SELECT gume.*, proizvodjaci.naziv AS proizvodjac 
        FROM gume 
        JOIN proizvodjaci ON gume.proizvodjac_id = proizvodjaci.id
        WHERE popust > 0
    """
    
    kursor.execute(upit)
    gume_na_akciji = kursor.fetchall()
    
    kursor.close()
    konekcija.close()
    
    
    return render_template('proizvodi.html', gume=gume_na_akciji)

# ADMIN PANEL 

# Prikaz svih servisa
@app.route('/admin/servisi')
def admin_servisi():
    if 'korisnik_id' not in session or session.get('uloga') != 'admin':
        return redirect('/')
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
    # Povlacimo sve servise, najnoviji su na vrhu
    kursor.execute("SELECT * FROM zakazivanje_servisa ORDER BY datum_kreiranja DESC")
    svi_servisi = kursor.fetchall()
    kursor.close()
    konekcija.close()
    
    return render_template('admin_servisi.html', servisi=svi_servisi)

# Menjanje statusa
@app.route('/admin/azuriraj_status/<int:servis_id>', methods=['POST'])
def azuriraj_status(servis_id):
    novi_status = request.form.get('novi_status')
    
    konekcija = get_db_connection()
    kursor = konekcija.cursor()
    # Menjamo status u bazi za taj specificni ID
    upit = "UPDATE zakazivanje_servisa SET status = %s WHERE id = %s"
    kursor.execute(upit, (novi_status, servis_id))
    konekcija.commit()
    kursor.close()
    konekcija.close()
    
    return redirect(url_for('admin_servisi'))

# Prikaz svih korisnika u admin panelu
@app.route('/admin/korisnici')
def admin_korisnici():
    # Zastita: Samo admini mogu da pristupe
    if 'korisnik_id' not in session or session.get('uloga') != 'admin':
        return redirect('/')
    
    konekcija = get_db_connection()
    kursor = konekcija.cursor(dictionary=True)
    # Povlacimo sve korisnike iz baze
    kursor.execute("SELECT id, ime, email, uloga FROM korisnici_login_info")
    svi_korisnici = kursor.fetchall()
    kursor.close()
    konekcija.close()
    
    return render_template('admin_korisnici.html', korisnici=svi_korisnici)

# Menjanje uloge korisniku
@app.route('/admin/promeni_ulogu/<int:korisnik_id>', methods=['POST'])
def promeni_ulogu(korisnik_id):
    if 'korisnik_id' not in session or session.get('uloga') != 'admin':
        return redirect('/')

    # Zastita: Sprecavamo admina da slucajno obrise sam sebi prava i zakljuca se
    if korisnik_id == session['korisnik_id']:
        return "Ne možete sami sebi promeniti ulogu!", 400

    nova_uloga = request.form.get('nova_uloga')
    
    konekcija = get_db_connection()
    kursor = konekcija.cursor()
    # Menjamo ulogu u bazi
    kursor.execute("UPDATE korisnici_login_info SET uloga = %s WHERE id = %s", (nova_uloga, korisnik_id))
    konekcija.commit()
    kursor.close()
    konekcija.close()
    
    return redirect(url_for('admin_korisnici'))


# Pokretanje servera
if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def home():
    return "Hello"