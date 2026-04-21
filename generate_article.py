#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帖子生成自动化脚本
功能：
1. 生成帖子 HTML
2. 更新 index.html 精选内容（最多6个）
3. 更新 sitemap.xml
4. 自动推送到 GitHub

用法: python generate_article.py
"""

import os
import re
import http.server
import socketserver
import webbrowser
from datetime import datetime

# ============ 配置区 - 修改这里来生成新帖子 ============

# 帖子标题
POST_TITLE = "金边洗浴中心推荐"

# 帖子标签
POST_TAGS = ["金边洗浴", "洗浴中心", "水汇推荐", "泡澡推荐"]

# 发布日期
POST_DATE = datetime.now().strftime("%Y-%m-%d")

# ============ 帖子内容 ============

INTRO = "金边洗浴中心以其多样化的服务和舒适的环境受到广大游客和本地居民的青睐。本文为您推荐金边几家值得一试的洗浴中心。"

WHY_CHOOSE = "为什么选择金边洗浴中心？"

WHY_POINTS = [
    "设施完善，包含泡池、桑拿、休息区等一站式服务",
    "环境干净整洁，服务态度热情周到",
    "价格透明合理，性价比高于单独项目组合",
    "适合团建聚会或家庭休闲放松"
]

# 价格表格数据
MARKET_DATA = [
    ("基础洗浴", "$15-30", "60分钟", "含泡池+桑拿"),
    ("高级套餐", "$40-60", "90分钟", "洗浴+按摩组合"),
    ("VIP套房", "$80-120", "120分钟",  "私人包间+全套服务"),
    ("过夜套餐", "$100-150", "过夜", "含自助餐+休息大厅")
]

# 底部标签
ARTICLE_TAGS = [
    "金边洗浴中心",
    "金边洗浴推荐",
    "柬埔寨泡澡",
    "金边桑拿",
    "水汇会所",
    "金边休闲"
]

# ============ GitHub 配置 ============
GITHUB_TOKEN = "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"
GITHUB_REPO = "KKKyyyss2/ygsme-seo-website"
GITHUB_BRANCH = "main"

# 网站基础路径
SITE_URL = "https://xko1.com"

# ============ 路径配置 ============
# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEBSITE_DIR = SCRIPT_DIR  # 脚本直接在 ygsme-seo-website 目录下
POSTS_DIR = os.path.join(WEBSITE_DIR, "posts")
INDEX_FILE = os.path.join(WEBSITE_DIR, "index.html")
SITEMAP_FILE = os.path.join(WEBSITE_DIR, "sitemap.xml")

# ============ 代码区 - 不需要修改 ============


def generate_html_filename(title: str) -> str:
    """生成文件名：article-20260421-标题.html"""
    date_str = datetime.now().strftime("%Y%m%d")
    safe_title = ''.join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in title)
    safe_title = safe_title.replace(' ', '-')
    return f"article-{date_str}-{safe_title}.html"


def generate_canonical_url(filename: str) -> str:
    """生成 canonical URL"""
    return f"{SITE_URL}/posts/{filename}"


def generate_html(title: str, tags: list, date: str) -> str:
    """生成完整 HTML"""
    filename = generate_html_filename(title)
    
    why_items = ''.join(f"<li>{point}</li>" for point in WHY_POINTS)
    
    table_rows = ''
    for row in MARKET_DATA:
        table_rows += f"""                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                </tr>
"""
    
    tag_links = ''.join(f'            <a href="#">#{tag}</a>\n' for tag in ARTICLE_TAGS)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - 金边水汇会所">
    <meta name="keywords" content="{', '.join(tags)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{generate_canonical_url(filename)}">
    <title>{title} - 金边会所导航 | 高端按摩、水汇、SPA推荐 - 柬埔寨会所指南</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header class="hero">
        <div class="container">
            <h1>金边会所导航 | 高端按摩、水汇、SPA推荐 - 柬埔寨会所指南</h1>
            <p class="subtitle">按摩 | 水汇 | SPA | 会所推荐 - 金边、西港、波贝、财通、木牌、戈公</p>
            <p class="description">专注柬埔寨金边水汇服务，每日推荐优质按摩会所、马杀鸡场所，提供技师质量、价格透明、避坑指南，让你少走弯路。</p>
            <a href="https://t.me/s/ygsme" class="cta-button" target="_blank">关注Telegram频道</a>
        </div>
    </header>
    
    <nav class="nav-bar">
        <div class="container">
            <a href="../index.html">首页</a>
            <a href="../pages/gao-duan.html">高端推荐</a>
            <a href="../pages/bi-keng.html">避坑指南</a>
            <a href="../pages/ji-shi.html">技师质量</a>
            <a href="../pages/jia-ge.html">价格指南</a>
            <a href="../pages/xin-shou.html">新手指南</a>
            <a href="../pages/faq.html">FAQ</a>
        </div>
    </nav>

    <main class="container article-page">
        <a href="../index.html" class="back-link">返回首页</a>
        <div class="article-header">
            <span class="tag">金边水汇会所</span>
            <h1>{title}</h1>
            <p class="meta">发布日期：{date} | 来源：金边水汇会所原创</p>
        </div>

        <div class="article-content">
            <h2>引言</h2>
            <p>{INTRO}</p>

            <h2>{WHY_CHOOSE}</h2>
            <ul>
                {why_items}
            </ul>

            <h2>数据参考</h2>
            <table>
                <tr>
                    <th>档次</th>
                    <th>价格范围</th>
                    <th>技师质量</th>
                    <th>环境设施</th>
                </tr>
{table_rows}            </table>
        </div>

        <div class="article-tags">
            <h3>标签</h3>
            {tag_links}        </div>

        <div class="article-contact">
            <h3>投稿与合作</h3>
            <p>欢迎通过 Telegram 联系：<a href="https://t.me/JW469" target="_blank">@JW469</a></p>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 金边会所导航</p>
        </div>
    </footer>
</body>
</html>'''
    return html


def update_index_html(filename: str, title: str, description: str, date: str):
    """更新 index.html 精选内容，最多6个卡片"""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取前60个字符作为描述
    desc = description[:60] + "..." if len(description) > 60 else description
    
    new_card = f'''                <article class="post-card">
                    <h3><a href="posts/{filename}">{title}</a></h3>
                    <p>{desc}</p>
                    <span class="meta">发布日期：{date}</span>
                    <a href="posts/{filename}" class="read-more">阅读更多</a>
                </article>
'''
    
    # 查找 posts-grid 的开始位置
    pattern = r'(<div class="posts-grid">)'
    match = re.search(pattern, content)
    if not match:
        print("[ERROR] 未找到 posts-grid")
        return False
    
    insert_pos = match.end()
    
    # 在第一个 article 之前插入新卡片
    new_content = content[:insert_pos] + '\n' + new_card + content[insert_pos:]
    
    # 统计 article 数量，如果超过6个，删除最后一个
    article_matches = re.findall(r'<article class="post-card">', new_content)
    
    while len(article_matches) > 6:
        # 找到最后一个 </article> 之前的位置
        last_article_end = new_content.rfind('</article>')
        prev_content = new_content[:last_article_end]
        last_article_start = prev_content.rfind('<article class="post-card">')
        
        new_content = new_content[:last_article_start] + new_content[last_article_end + len('</article>'):]
        article_matches = re.findall(r'<article class="post-card">', new_content)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] index.html 已更新，现有 {len(article_matches)} 个卡片")
    return True


def update_sitemap(filename: str, date: str):
    """更新 sitemap.xml"""
    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_url = f'''
  <url>
    <loc>{SITE_URL}/posts/{filename}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
'''
    
    # 在 </urlset> 之前插入新 URL
    new_content = content.replace('</urlset>', new_url + '</urlset>')
    
    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("[OK] sitemap.xml 已更新")


def git_push():
    """推送更新到 GitHub"""
    import subprocess
    
    os.chdir(WEBSITE_DIR)
    
    # 添加所有更改
    subprocess.run(['git', 'add', '.'], check=True)
    
    # 提交
    commit_msg = f"Update: 添加新帖子 {POST_TITLE} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True, text=True)
    
    # 推送
    remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    subprocess.run(['git', 'push', remote_url, f'HEAD:{GITHUB_BRANCH}'], check=True, capture_output=True, text=True)
    
    print("[OK] 已推送到 GitHub")
    return True


def main():
    print("=" * 50)
    print("[INFO] 帖子生成自动化脚本")
    print("=" * 50)
    
    # 1. 生成 HTML 文件
    filename = generate_html_filename(POST_TITLE)
    filepath = os.path.join(POSTS_DIR, filename)
    html_content = generate_html(POST_TITLE, POST_TAGS, POST_DATE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"[OK] 帖子已生成: {filename}")
    
    # 2. 更新 index.html
    update_index_html(filename, POST_TITLE, INTRO, POST_DATE)
    
    # 3. 更新 sitemap.xml
    update_sitemap(filename, POST_DATE)
    
    # 4. 推送到 GitHub
    print("[INFO] 正在推送到 GitHub...")
    try:
        git_push()
        print("\n" + "=" * 50)
        print("[SUCCESS] 完成！所有步骤执行成功！")
        print("=" * 50)
    except Exception as e:
        print(f"[ERROR] 推送失败: {e}")
        print("[INFO] 文件已生成，但未推送到 GitHub")


if __name__ == "__main__":
    main()
