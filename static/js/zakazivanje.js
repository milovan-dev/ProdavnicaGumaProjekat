document.querySelector('.zakazivanje-forma').addEventListener('submit', function(event) {

        //Regex ime i prezime
        const imePrezime = document.querySelector('input[name="ime_prezime"]').value.trim();//dohvata ime i prezime i trimuje razmak posle poslednjeg slova
        if (!imePrezime.includes(' ')) {//trazi razmak, ! znaci negaciju, ako ima razmak nastavi sa izvrsavanjem
            alert('Greška: Razdvojte ime i prezime razmakom!');
            event.preventDefault();//zaustavljanje slanja forme
        }

        //Regex telefona
        const telefon = document.querySelector('input[name="telefon"]').value;//dohvata telefon
        const telefonRegex = /^06\d{7,8}$/; /*pocinje sa 06, nakon toga 7 ili 8 karaktera*/

        if (!telefonRegex.test(telefon)) {
            alert('Greška: Telefon nije u validnom formatu!');
            event.preventDefault();
        }

        //Regex mejl
        const mail = document.querySelector('input[name="email"]').value;//dohvata mejl
        if(!mail.includes('@')||!mail.includes('.')){//mora da sadrzi @ i .
            alert('Greska: Unesite ispravan format mejl adrese');
            event.preventDefault();
        }

        //Regex datuma
        const datumInput = document.querySelector('input[name="datum_servisa"]').value;//dohvata datum 
        const danas = new Date().toISOString().split('T')[0];//danasnji datum
        
        if (datumInput < danas) {
            alert('Greška: Datum servisa ne može biti u prošlosti!');
            event.preventDefault();
        }

    });