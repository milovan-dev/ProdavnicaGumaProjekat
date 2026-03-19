Web Sajt TireShop&Servis Čačak namenjen je prodaji auto guma i pružanju usluga auto servisa i vulkanizerska radnja. Sajt omogućava korisnicima da pregledaju ponudu guma po dimenziji, proizvođaču i sezoni za koju je guma namenjena, kao i da dobiju informacije o dostupnim servisnim uslugama.
Takodje cilj sajta je da omogući zakazivanje termina za mali servis, veliki servis, servis kočionog sistema i vulkanizerske usluge kao i pregled korpe odnosno proizvoda za koje se kupac odlučio.

Kako sajt funkcioniše:
Korisnik ima više načina da izabere gume koje su mu potrebne.
Na početnoj stranici odmah mu se pojavljuje deo za pretragu guma gde moze izabrati širinu, visinu, prečnik i sezonu za koju je sama guma namenjena.
Drugi način je da klikom na stranicu gume može izabrati gume sam skrolovanjem stranice ili sa desne strane uraditi filtraciju sa gore pomenutim filterima.
Nakon što korisnik izabere odgovarajuće gume one se prikazuju u korpi i nakon klika na korpu korisnik potvrđuje kupovinu ili može da nastavi sa dodavanjem guma i kasnije završi kupovinu.
Završetak kupovine se realizuje na način tako što korisnik unese potrebne informaciju u formu za unos kao što su ime i prezime, adresa za dostavu i broj telefona.

Takođe na sajtu je moguće zakazati servisne usluge na stranici servis gde se pojavljuje padajući meni i korisnik bira servis.
Nakon odabira servisa korisnik popunjava formu i bira datum servisa.

Tehnologije korišćene u izdradi sajta:


----Preuzimanje i instalacija potrebnih programa

Da biste pokrenuli ovaj projekat na svom računaru, potrebno je da imate instalirana sledeća tri programa. Ukoliko ih nemate, preuzmite ih sa priloženih linkova:

Visual Studio Code 
-Preuzimanje: https://code.visualstudio.com/

----Python
Python:
-Preuzimanje: https://www.python.org/downloads/
-VAŽNO PRI INSTALACIJI: Kada pokrenete instalaciju, na samom prvom prozorčiću na dnu ekrana OBAVEZNO štiklirajte opciju `Add Python to PATH`(ili `Add python.exe to PATH`)

----XAMPP

XAMPP nam omogućava da napravimo lokalni server i koristimo MySQL bazu podataka na našem kompjuteru.

-Preuzimanje: https://www.apachefriends.org/index.html
-Pokretanje: Nakon instalacije, otvorite XAMPP Control Panel i kliknite na dugme Start pored modula Apache i MySQL.
-Zatim u pretraživaču idite na `http://localhost/phpmyadmin/` kako biste uvezli bazu podataka.

--Dodavanje baze u MYSQL:

-Bazu mozete dodati tako sto pristupite http://localhost/phpmyadmin/ i kliknete na +New i za ime stavite prodavnica_guma i izaberite utf8mb4_general_ci zatim kliknite na create.
-Zatim kliknite na tu novu bazu i kliknite na karticu Import, izaberite choose file i izaberite Bazu koja se nalazi u folderu projekta, zatim kliknete na import.

---

----Tehnologije korišćene u izradi sajta

-Frontend (Izgled i interaktivnost klijentske strane)

-HTML5:
-CSS3:
-JavaScript (JS):
-AJAX (Fetch API)- dodavanje proizvoda u korpu bez osvezavanja stranice

---- Backend (Serverska logika aplikacije)
-Python: Glavni programski jezik zadužen za obradu podataka, logiku korpe i komunikaciju sa bazom.
-Flask: backend framework
-Jinja2: Omogućava nam da unutar HTML fajlova koristimo Python komande (poput `if` uslova i `for` petlji) kako bismo dinamički prikazivali proizvode iz baze.

----Baza podataka
-MySQL: Relaciona baza podataka u kojoj trajno čuvamo sve informacije o korisnicima, proizvodima, trenutnim cenama u korpi i zakazanim servisima.

---

----Pokretanje aplikacije

1. Otvorite folder projekta u **Visual Studio Code-u**.
2. Otvorite terminal unutar editora (`Terminal -> New Terminal`).
3. Instalirajte potrebne dodatke (Upustvo se nalazi u requirements.txt file-u)
   
-Zatim pokrecemo server tako sto napisemo sledecu komandu u terminal python server.py

-U terminalu ce se pojaviti adresa http://127.0.0.1:5000 zadrzimo ctrl i kliknemo na tu adresu

-Kada vlasnik/admin zeli da promeni status nekog zakazanog servisa, to moze da uradi tako sto ukuca sledecu adresu http://127.0.0.1:5000/admin/servisi
-Na toj adresi imace meni na kojem moze da menja status servisa vozila koji ce automatski da azurira bazu podataka.







