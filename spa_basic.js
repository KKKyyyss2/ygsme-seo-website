// SPA Navigation Script for xko1.com
document.addEventListener('DOMContentLoaded', function() {
    const spaContainer = document.getElementById('spa-container');
    const navLinks = document.querySelectorAll('nav a');
    
    function loadPage(url) {
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.getElementById('spa-container');
                if (newContent) {
                    spaContainer.innerHTML = newContent.innerHTML;
                    window.history.pushState({}, '', url);
                }
            })
            .catch(error => console.error('Error loading page:', error));
    }
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            if (href && !href.startsWith('http')) {
                loadPage(href);
            }
        });
    });
    
    // Handle browser back/forward
    window.addEventListener('popstate', function() {
        loadPage(window.location.pathname);
    });
});
