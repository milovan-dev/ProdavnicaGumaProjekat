import mysql.connector

# Povezivanje na bazu
konekcija = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="prodavnica_guma"
)
kursor = konekcija.cursor()

print("Povezivanje sa bazom uspešno. Započinjem unos podataka...")

# 1. Spisak svih 10 brendova sa sajta
brendovi = [
    ('Michelin', 'Francuska'), ('Sava', 'Slovenija'), ('Tigar', 'Srbija'),
    ('Pirelli', 'Italija'), ('Continental', 'Nemačka'), ('Dunlop', 'Velika Britanija'),
    ('Goodyear', 'SAD'), ('Hankook', 'Južna Koreja'), ('Lassa', 'Turska'),
    ('Bridgestone', 'Japan')
]

# Ubacujemo brendove ako već ne postoje
for naziv, zemlja in brendovi:
    kursor.execute("SELECT id FROM proizvodjaci WHERE naziv = %s", (naziv,))
    if not kursor.fetchone():
        kursor.execute("INSERT INTO proizvodjaci (naziv, zemlja_porekla) VALUES (%s, %s)", (naziv, zemlja))
konekcija.commit()

kursor.execute("SELECT naziv, id FROM proizvodjaci")
proizvodjaci_mapa = {red[0]: red[1] for red in kursor.fetchall()}

# 2. Tacni i realisticni podaci za 40 guma (Brend, Kategorija, Model, Sirina, Visina, Precnik, Sezona, Cena)
# Kategorije: 1 = Putnicka, 2 = Dzip/SUV, 3 = Kombi
gume_podaci = [
    # Michelin
    ('Michelin', 1, 'Alpin 6', 195, 65, 15, 'Zimska', 11000),
    ('Michelin', 1, 'Pilot Sport 5', 225, 45, 17, 'Letnja', 16500),
    ('Michelin', 1, 'CrossClimate 2', 205, 55, 16, 'Sve sezone', 13500),
    ('Michelin', 2, 'Pilot Alpin 5 SUV', 235, 60, 18, 'Zimska', 21000),
    # Sava
    ('Sava', 1, 'Eskimo S3+', 195, 65, 15, 'Zimska', 5500),
    ('Sava', 1, 'Intensa HP2', 205, 55, 16, 'Letnja', 6000),
    ('Sava', 1, 'All Weather', 205, 55, 16, 'Sve sezone', 6500),
    ('Sava', 2, 'Eskimo SUV 2', 225, 65, 17, 'Zimska', 10500),
    # Tigar
    ('Tigar', 1, 'Winter', 195, 65, 15, 'Zimska', 4800),
    ('Tigar', 1, 'High Performance', 205, 55, 16, 'Letnja', 5200),
    ('Tigar', 1, 'All Season', 205, 55, 16, 'Sve sezone', 5600),
    ('Tigar', 3, 'CargoSpeed Winter', 205, 75, 16, 'Zimska', 8000),
    # Pirelli
    ('Pirelli', 1, 'Cinturato Winter 2', 205, 55, 16, 'Zimska', 12000),
    ('Pirelli', 1, 'P Zero', 225, 45, 17, 'Letnja', 17000),
    ('Pirelli', 1, 'Cinturato All Season SF2', 205, 55, 16, 'Sve sezone', 14000),
    ('Pirelli', 2, 'Scorpion Winter', 235, 60, 18, 'Zimska', 22000),
    # Continental
    ('Continental', 1, 'WinterContact TS 870', 205, 55, 16, 'Zimska', 13000),
    ('Continental', 1, 'PremiumContact 7', 225, 45, 17, 'Letnja', 16000),
    ('Continental', 1, 'AllSeasonContact', 205, 55, 16, 'Sve sezone', 14500),
    ('Continental', 2, 'CrossContact ATR', 235, 65, 17, 'Letnja', 19000),
    # Dunlop
    ('Dunlop', 1, 'Winter Response 2', 195, 65, 15, 'Zimska', 9500),
    ('Dunlop', 1, 'Sport Bluresponse', 205, 55, 16, 'Letnja', 10500),
    ('Dunlop', 1, 'Sport All Season', 225, 45, 17, 'Sve sezone', 12500),
    ('Dunlop', 2, 'Winter Sport 5 SUV', 235, 60, 18, 'Zimska', 18500),
    # Goodyear
    ('Goodyear', 1, 'UltraGrip 9+', 195, 65, 15, 'Zimska', 10000),
    ('Goodyear', 1, 'EfficientGrip Performance 2', 205, 55, 16, 'Letnja', 11500),
    ('Goodyear', 1, 'Vector 4Seasons Gen-3', 225, 45, 17, 'Sve sezone', 13000),
    ('Goodyear', 2, 'UltraGrip Performance+ SUV', 235, 60, 18, 'Zimska', 20000),
    # Hankook
    ('Hankook', 1, 'Winter i*cept RS3', 205, 55, 16, 'Zimska', 8500),
    ('Hankook', 1, 'Ventus Prime 4', 225, 45, 17, 'Letnja', 9500),
    ('Hankook', 1, 'Kinergy 4S2', 205, 55, 16, 'Sve sezone', 10000),
    ('Hankook', 2, 'Winter i*cept evo3 X', 235, 60, 18, 'Zimska', 16000),
    # Lassa
    ('Lassa', 1, 'Snoways 4', 205, 55, 16, 'Zimska', 6500),
    ('Lassa', 1, 'Greenways', 195, 65, 15, 'Letnja', 6000),
    ('Lassa', 1, 'Multiways 2', 205, 55, 16, 'Sve sezone', 7000),
    ('Lassa', 2, 'Competus Winter 2', 225, 65, 17, 'Zimska', 11000),
    # Bridgestone
    ('Bridgestone', 1, 'Blizzak LM005', 205, 55, 16, 'Zimska', 12500),
    ('Bridgestone', 1, 'Turanza T005', 225, 45, 17, 'Letnja', 14500),
    ('Bridgestone', 1, 'Weather Control A005', 205, 55, 16, 'Sve sezone', 13500),
    ('Bridgestone', 2, 'Blizzak LM-80 EVO', 235, 60, 18, 'Zimska', 21500)
]

brojac = 0
for guma in gume_podaci:
    brend, kategorija_id, model, sirina, visina, precnik, sezona, cena = guma
    proizvodjac_id = proizvodjaci_mapa.get(brend)
    
    # Dodeljujemo sliku na osnovu sezone 
    if sezona == 'Zimska':
        slika_url = 'lassa_snoways.jpg'
    elif sezona == 'Letnja':
        slika_url = 'lassa_greenways.jpg'
    else:
        slika_url = 'pirelli_cinturato.jpg'
        
    sql = """INSERT INTO gume (proizvodjac_id, kategorija_id, model, sirina, visina, precnik, sezona, cena, kolicina_na_stanju, slika_url) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 20, %s)"""
    
    kursor.execute(sql, (proizvodjac_id, kategorija_id, model, sirina, visina, precnik, sezona, cena, slika_url))
    brojac += 1

konekcija.commit()
kursor.close()
konekcija.close()

print(f"Uspesno zavrseno! Ubaceno je {brojac} realističnih modela guma u bazu podataka.")