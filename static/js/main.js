// 1. ANIMACIJE NA SKROL
document.addEventListener("DOMContentLoaded", () => { 
    // Kod se izvrsava tek kad se cela stranica ucita
    const hiddenElements = document.querySelectorAll('.hidden');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('show');
            } else {
                entry.target.classList.remove('show'); // Animacija se ponavlja skrolom na gore
            }
        });
    }, { threshold: 0.1 }); // Aktivira se na 10% vidljivosti elementa

    hiddenElements.forEach((el) => observer.observe(el));
});

// 2. AJAX ZA DODAVANJE U KORPU
document.addEventListener('submit', function(e) {
    if (e.target && e.target.classList.contains('forma-korpa')) {
        e.preventDefault(); // Sprecava pretrazivac da osvezi stranicu

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
                document.querySelectorAll('.korpa-brojac').forEach(brojac => {
                    brojac.innerText = data.broj_u_korpi;
                });

                
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