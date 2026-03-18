function toggleMeni() {
    document.querySelector('.meni').classList.toggle('aktivan');
}

//Ajax 
document.addEventListener('submit', function(e) {
    if (e.target && e.target.classList.contains('forma-korpa')) {
        e.preventDefault(); 

        const forma = e.target;
        const dugme = forma.querySelector('button');
        const url = forma.action;

        fetch(url, {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' } 
        })
        .then(response => response.json())
        .then(data => {
            if (data.uspeh) {
                // Ažurira sve brojače  kroz forEach
                document.querySelectorAll('.korpa-brojac').forEach(brojac => {
                    brojac.innerText = data.broj_u_korpi;
                });

                //Povratna info na dugmetu
                const originalText = dugme.innerText;
                dugme.innerText = "Dodato! ✅";
                dugme.style.backgroundColor = "#28a745"; 
                
                setTimeout(() => {
                    dugme.innerText = originalText;
                    dugme.style.backgroundColor = "";
                }, 2000);
            }
        })
        .catch(error => console.error("Došlo je do greške:", error));
    }
});
    
    