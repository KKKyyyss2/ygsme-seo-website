     1|// SPA导航核心脚本 - 全站统一
     2|(function() {
     3|    const container = document.getElementById('spa-container');
     4|    if (!container) return; // 如果没有spa-container，不执行SPA逻辑
     5|
     6|    function loadPage(path, push = true) {
     7|        let url;
     8|        if (path === '/' || path === '/index.html' || path === '') {
     9|            url = '/index.html';
    10|        } else if (path.startsWith('/article-')) {
    11|            // 文章文件在articles/目录下
    12|            url = '/articles' + path + '.html';
    13|        } else {
    14|            url = path + '.html';
    15|        }
    16|        
    17|        fetch(url, {headers: {'X-Requested-With': 'XMLHttpRequest'}})
    18|            .then(r => {
    19|                if (!r.ok) throw new Error('HTTP ' + r.status);
    20|                return r.text();
    21|            })
    22|            .then(html => {
    23|                const parser = new DOMParser();
    24|                const doc = parser.parseFromString(html, 'text/html');
    25|                const newContent = doc.getElementById('spa-container').innerHTML;
    26|                container.innerHTML = newContent;
    27|                if (push) history.pushState(null, '', path);
    28|                setActive(path);
    29|                // 触发自定义事件，让页面知道SPA导航完成
    30|                window.dispatchEvent(new CustomEvent('spa-navigate', { detail: { path } }));
    31|            })
    32|            .catch(err => {
    33|                console.error('SPA page load error:', err);
    34|                // 降级：直接跳转
    35|                window.location.href = path;
    36|            });
    37|    }
    38|
    39|    function setActive(path) {
    40|        let p = path;
    41|        if (p === '/index.html' || p === '') p = '/';
    42|        if (!p.startsWith('/')) p = '/' + p;
    43|        document.querySelectorAll('.nav-bar a').forEach(a => {
    44|            a.classList.toggle('active', a.getAttribute('href') === p);
    45|        });
    46|    }
    47|
    48|    // 点击导航拦截
    49|    document.addEventListener('click', (e) => {
    50|        const a = e.target.closest('a');
    51|        if (!a) return;
    52|        const href = a.getAttribute('href');
    53|        if (!href || href.startsWith('http') || a.target === '_blank' || href.startsWith('#')) return;
    54|        
    55|        const linkUrl = new URL(href, window.location.origin);
    56|        if (linkUrl.origin !== window.location.origin) return;
    57|        
    58|        e.preventDefault();
    59|        loadPage(linkUrl.pathname);
    60|    });
    61|
    62|    // 浏览器前进后退支持
    63|    window.addEventListener('popstate', () => {
    64|        loadPage(window.location.pathname, false);
    65|    });
    66|
    67|    // 初始设置当前活动导航
    68|    setActive(window.location.pathname);
    69|
    70|    // 全局导出loadPage函数，供其他脚本调用
    71|    window.spaLoadPage = loadPage;
    72|})();