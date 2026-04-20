// SPA导航核心脚本 - 全站统一
(function() {
    const container = document.getElementById('spa-container');
    if (!container) return; // 如果没有spa-container，不执行SPA逻辑

    function loadPage(path, push = true) {
        let url;
        if (path === '/' || path === '/index.html' || path === '') {
            url = '/index.html';
        } else if (path.startsWith('/article-')) {
            // 文章文件在articles/目录下
            url = '/articles' + path + '.html';
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
                // 触发自定义事件，让页面知道SPA导航完成
                window.dispatchEvent(new CustomEvent('spa-navigate', { detail: { path } }));
            })
            .catch(err => {
                console.error('SPA page load error:', err);
                // 降级：直接跳转
                window.location.href = path;
            });
    }

    function setActive(path) {
        let p = path;
        if (p === '/index.html' || p === '') p = '/';
        if (!p.startsWith('/')) p = '/' + p;
        document.querySelectorAll('.nav-bar a').forEach(a => {
            a.classList.toggle('active', a.getAttribute('href') === p);
        });
    }

    // 点击导航拦截
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

    // 浏览器前进后退支持
    window.addEventListener('popstate', () => {
        loadPage(window.location.pathname, false);
    });

    // 初始设置当前活动导航
    setActive(window.location.pathname);

    // 全局导出loadPage函数，供其他脚本调用
    window.spaLoadPage = loadPage;
})();