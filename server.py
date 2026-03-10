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


if __name__ == '__main__':
    
    app.run(debug=True)