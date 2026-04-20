(function() {
    const container = document.getElementById('spa-container');

    function loadPage(path, push = true) {
        let url;
        if (path === '/' || path === '/index.html' || path === '') {
            url = '/index.html';
        } else if (path.startsWith('/article-')) {
            url = path + '.html';
        } else {
            url = path + '.html';
        }
        fetch(url, {headers: {'X-Requested-With': 'XMLHttpRequest'}})
            .then(r => {
                if (!r.ok) throw new Error('HTTP ' + r.status);
                return r.text();
            })
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.getElementById('spa-container').innerHTML;
                container.innerHTML = newContent;
                if (push) history.pushState(null, '', path);
                setActive(path);
            })
            .catch(err => console.error('Page load error:', err));
    }

    function setActive(path) {
        let p = path;
        if (p === '/index.html' || p === '') p = '/';
        if (!p.startsWith('/')) p = '/' + p;
        document.querySelectorAll('.nav-bar a').forEach(a => {
            a.classList.toggle('active', a.getAttribute('href') === p);
        });
    }

    document.addEventListener('click', (e) => {
        const a = e.target.closest('a');
        if (!a) return;
        const href = a.getAttribute('href');
        if (!href || href.startsWith('http') || a.target === '_blank' || href.startsWith('#')) return;
        const linkUrl = new URL(href, window.location.origin);
        if (linkUrl.origin !== window.location.origin) return;
        e.preventDefault();
        loadPage(linkUrl.pathname);
    });

    window.addEventListener('popstate', () => {
        loadPage(location.pathname, false);
    });

    setActive(location.pathname);
})();
