document.querySelector('.zakazivanje-forma').addEventListener('submit', function(event){

    //Regex za Ime i Prezime
    const ime_prezime = document.querySelector('input[name="ime_prezime"]').value.trim();//trim odseca razmak posle posldnjeg slova
    if(!ime_prezime.includes(' ')){
        alert('Grska. Razdvojte ime i prezime razmakom!');
        event.preventDefault();
    }

    //Regex za adresu
    const adresa = document.querySelector('input[name="adresa"]').value;
    const adresaRegex=/\d/; //mora da sadrzi broj
    if (!adresaRegex.test(adresa)) { //proverava da li se nalazi broj u unosu
        alert('Greška. Unesite broj u adresu!');
        event.preventDefault();
    }

    //Regex za broj telefona
    const telefon=document.querySelector('input=["telefon"]').value;
    const telefonRegex=/^06\d{7,8}$/;//pocinje sa 06 i ima posle toga 7 ili 8 karatktera
    if(!telefonRegex.test(telefon)){
        alert('Greska. Telefon nije u validnom formatu!');
        event.preventDefault();
    }
});