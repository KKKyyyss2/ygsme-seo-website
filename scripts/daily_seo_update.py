#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日SEO更新脚本 - 金边会所网站
功能：生成新文章、更新首页精选内容、更新sitemap.xml、推送GitHub
作者：Hermes Agent
日期：2026-04-21
"""

import os
import re
import json
import random
import datetime
import subprocess
from pathlib import Path

# ==================== 配置参数 ====================
脚本目录 = Path(__file__).parent.absolute()
SITE_ROOT = 脚本目录.parent  # 网站根目录
ARTICLES_DIR = SITE_ROOT  # 文章在根目录
INDEX_FILE = SITE_ROOT / "index.html"
SITEMAP_FILE = SITE_ROOT / "sitemap.xml"
SCRIPTS_DIR = 脚本目录

# ==================== 模板函数 ====================
def 生成文章HTML模板(文章数据):
    """生成完整的文章HTML页面"""
    模板 = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{文章数据['描述']}">
    <meta name="keywords" content="{文章数据['关键词']}">
    <title>{文章数据['标题']} - 金边会所导航 | 高端按摩、水汇、SPA推荐 - 柬埔寨会所指南</title>
    <link rel="stylesheet" href="/style.css">
    <link rel="canonical" href="https://xko1.com/{文章数据['文件名']}">
    <link rel="sitemap" type="application/xml" href="/sitemap.xml">
    <script src="/spa.js" defer></script>
</head>
<body>
    <header class="hero">
  <div class="container">
<div class="container">
            <h1>金边会所导航 | 高端按摩、水汇、SPA推荐 - 柬埔寨会所指南</h1>
            <p class="subtitle">🇨🇳 按摩 | 水汇 | SPA  | 会所推荐 - 金边、西港、波贝、财通、木牌、戈公 🇰🇭</p>
            <p class="description">专注柬埔寨金边水汇服务，每日推荐优质按摩会所、马杀鸡场所，提供技师质量、价格透明、避坑指南，让你少走弯路。</p>
            <a href="https://t.me/s/ygsme" class="cta-button" target="_blank">👉 关注Telegram频道</a>
        </div>
  </div>
</header>

    <nav class="nav-bar">
        <div class="container">
            <a href="/">首页</a>
            <a href="/gao-duan">高端推荐</a>
            <a href="/bi-keng">避坑指南</a>
            <a href="/ji-shi">技师质量</a>
            <a href="/jia-ge">价格指南</a>
            <a href="/xin-shou">新手指南</a>
            <a href="/faq">FAQ</a>
        </div>
    </nav>

    <main id="spa-container" class="container">
        
        <article class="post-card">
{文章数据['内容']}
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <p>© 2026 金边会所导航 | 高端按摩、水汇、SPA推荐 - 柬埔寨会所指南</p>
            <p>联系我们: <a href="https://t.me/s/ygsme" target="_blank">Telegram频道</a></p>
        </div>
    </footer>
</body>
</html>'''
    return 模板

def 生成首页文章卡片(文章数据):
    """生成首页精选区域的文章卡片HTML"""
    卡片 = f'''<article class="post-card">
        <h3><a href="/{文章数据['文件名']}">{文章数据['标题']} - 金边水汇会所</a></h3>
        <p>{文章数据['描述']}</p>
        <a href="/{文章数据['文件名']}" class="read-more">阅读更多 ></a>
    </article>'''
    return 卡片

# ==================== 核心逻辑函数 ====================
def 检查重复文章(文章标题):
    """检查是否已有相同标题的文章"""
    # 获取所有现有文章文件
    现有文章 = []
    for 文件 in ARTICLES_DIR.glob("article-*.html"):
        try:
            with open(文件, 'r', encoding='utf-8') as f:
                内容 = f.read()
                # 从title标签提取标题
                title_match = re.search(r'<title>(.*?)</title>', 内容)
                if title_match:
                    现有标题 = title_match.group(1).split(' - ')[0].strip()
                    现有文章.append(现有标题)
        except:
            continue
    
    # 检查是否重复
    for 现有标题 in 现有文章:
        if 文章标题 in 现有标题 or 现有标题 in 文章标题:
            print(f"⚠️  发现相似文章: '{现有标题}'")
            return True
    
    return False

def 生成文章数据():
    """生成新的文章数据（标题、内容、关键词等）"""
    # 当前日期
    今天 = datetime.datetime.now()
    日期字符串 = 今天.strftime("%Y%m%d")
    
    # 随机生成文章ID
    随机ID = random.randint(100, 999)
    
    # 文章主题列表（纯中文）
    主题列表 = [
        "金边高端SPA会所推荐",
        "柬埔寨按摩技师质量分析",
        "西港水汇避坑指南",
        "波贝会所价格对比",
        "木牌按摩服务体验",
        "戈公休闲会所推荐",
        "金边足疗最新优惠",
        "柬埔寨水汇安全指南"
    ]
    
    主题 = random.choice(主题列表)
    
    # 生成文件名（不含.html扩展名）
    文件名 = f"article-{日期字符串}-{主题.replace(' ', '-')}-{随机ID}"
    
    # 生成文章内容（Markdown格式）
    内容 = f"""# {主题}

*更新于 {今天.strftime('%Y-%m-%d')} - 金边水汇会所原创*

---

## 引言

在金边，选择一家好的水汇会所或按摩店是享受休闲时光的关键。今天我们来详细聊聊{主题}。

---

## 主要内容

### 为什么重要？

金边的水汇会所众多，服务质量参差不齐。了解{主题}能帮助你做出更好的选择，避免踩坑。

### 详细分析

1. **市场现状**
   - 金边水汇会所数量众多
   - 价格从$20到$200+不等
   - 服务质量差异大

2. **选择建议**
   - 优先选择有正规牌照的会所
   - 查看谷歌地图评价（4.0以上）
   - 价格透明，无强制消费

3. **实用技巧**
   - 白天前往价格更低
   - 多人可议团体价
   - 提前电话确认费用

---

## 📊 数据参考

| 项目 | 低端 | 中端 | 高端 |
|------|------|------|------|
| 价格范围 | $20-50 | $50-100 | $100+ |
| 技师质量 | 一般 | 良好 | 优秀 |
| 环境设施 | 基础 | 舒适 | 豪华 |

---

## 💬 互动

你在金边有过相关经历吗？欢迎留言分享你的推荐或避坑经验！

**📮 投稿/合作**: [@JW469](https://t.me/s/ygsme)

---

## 搜索关键词

{主题},金边按摩,柬埔寨水汇,会所推荐
"""
    
    # 生成描述（截取前100字符）
    描述 = f"{主题} - 专注柬埔寨金边水汇服务，提供按摩、SPA、会所推荐与避坑指南。"
    
    # 生成关键词
    关键词 = f"{主题},金边按摩,柬埔寨水汇,会所推荐"
    
    return {
        "标题": 主题,
        "描述": 描述,
        "关键词": 关键词,
        "内容": 内容,
        "文件名": 文件名,
        "URL": f"https://xko1.com/{文件名}",
        "日期": 今天.strftime("%Y-%m-%d")
    }

def 更新首页精选内容(新文章卡片):
    """在首页插入新文章卡片，移除最旧的文章"""
    try:
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            首页内容 = f.read()
        
        # 找到精选文章区域
        # 查找 <section class="featured-posts"> 和对应的 </section>
        开始标记 = '<section class="featured-posts">'
        结束标记 = '</section>'
        
        开始位置 = 首页内容.find(开始标记)
        if 开始位置 == -1:
            print("❌ 找不到精选文章区域")
            return False
        
        # 找到这个section的结束位置
        结束位置 = 首页内容.find(结束标记, 开始位置)
        if 结束位置 == -1:
            print("❌ 找不到精选文章区域结束标记")
            return False
        
        # 提取整个featured-posts区域
        精选区域 = 首页内容[开始位置:结束位置 + len(结束标记)]
        
        # 找到posts-grid内的所有article
        # 查找 <div class="posts-grid"> 和 </div>
        网格开始 = 精选区域.find('<div class="posts-grid">')
        网格结束 = 精选区域.find('</div>', 网格开始)
        
        if 网格开始 == -1 or 网格结束 == -1:
            print("❌ 找不到posts-grid区域")
            return False
        
        网格内容 = 精选区域[网格开始:网格结束]
        
        # 提取现有的article卡片
        article_pattern = r'<article class="post-card">.*?</article>'
        现有卡片 = re.findall(article_pattern, 网格内容, re.DOTALL)
        
        if len(现有卡片) < 5:
            print(f"⚠️  现有卡片数量不足: {len(现有卡片)}")
            return False
        
        print(f"📊 现有文章卡片数量: {len(现有卡片)}")
        
        # 保留前4个（位置1-4），移除第5个
        保留卡片 = 现有卡片[:4]
        
        # 构建新的网格内容：新卡片 + 保留的4个卡片
        新网格内容 = f'<div class="posts-grid">\n{新文章卡片}\n'
        for 卡片 in 保留卡片:
            新网格内容 += f'{卡片}\n'
        新网格内容 += '</div>'
        
        # 替换原网格内容
        新精选区域 = 精选区域[:网格开始] + 新网格内容 + 精选区域[网格结束:]
        
        # 替换整个首页内容
        新首页内容 = 首页内容[:开始位置] + 新精选区域 + 首页内容[结束位置 + len(结束标记):]
        
        # 写回文件
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(新首页内容)
        
        print("✅ 首页精选内容更新成功")
        print(f"   - 新文章插入到位置1")
        print(f"   - 原位置1-4的文章后移")
        print(f"   - 原位置5的文章已移除")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新首页失败: {e}")
        return False

def 更新sitemap(新文章URL):
    """在sitemap.xml中添加新文章URL"""
    try:
        with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
            sitemap内容 = f.read()
        
        # 检查是否已存在该URL
        if 新文章URL in sitemap内容:
            print(f"⚠️  sitemap中已存在URL: {新文章URL}")
            return True
        
        # 找到最后一个</url>标签的位置
        最后url位置 = sitemap内容.rfind('</url>')
        if 最后url位置 == -1:
            print("❌ 找不到</url>标签")
            return False
        
        # 获取当前日期
        今天 = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # 构建新的URL条目
        新url条目 = f'''  <url>
    <loc>{新文章URL}</loc>
    <lastmod>{今天}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>'''
        
        # 插入新条目（在最后一个</url>之后，</urlset>之前）
        新sitemap内容 = sitemap内容[:最后url位置 + 6] + '\n' + 新url条目
        
        # 写回文件
        with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
            f.write(新sitemap内容)
        
        print(f"✅ sitemap.xml更新成功")
        print(f"   - 添加URL: {新文章URL}")
        print(f"   - 最后修改日期: {今天}")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新sitemap失败: {e}")
        return False

def 推送GitHub():
    """提交并推送到GitHub"""
    try:
        print("📤 开始GitHub推送流程...")
        
        # 1. 添加所有更改
        print("  1. 添加文件到暂存区...")
        git_add = subprocess.run(
            ["git", "add", "."],
            cwd=SITE_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if git_add.returncode != 0:
            print(f"❌ git add失败: {git_add.stderr}")
            return False
        
        # 2. 提交更改
        今天 = datetime.datetime.now().strftime("%Y-%m-%d")
        提交信息 = f"每日SEO更新: {今天} - 新增文章"
        
        print(f"  2. 提交更改: {提交信息}")
        git_commit = subprocess.run(
            ["git", "commit", "-m", 提交信息],
            cwd=SITE_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if git_commit.returncode != 0:
            # 可能没有更改需要提交
            if "nothing to commit" in git_commit.stdout or "nothing to commit" in git_commit.stderr:
                print("⚠️  没有更改需要提交")
                return True
            else:
                print(f"❌ git commit失败: {git_commit.stderr}")
                return False
        
        # 3. 推送到远程仓库
        print("  3. 推送到GitHub...")
        git_push = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=SITE_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if git_push.returncode != 0:
            print(f"❌ git push失败: {git_push.stderr}")
            return False
        
        print("✅ GitHub推送成功")
        print(f"   - 提交信息: {提交信息}")
        print(f"   - 分支: main")
        
        return True
        
    except Exception as e:
        print(f"❌ GitHub推送失败: {e}")
        return False

# ==================== 主函数 ====================
def 主流程():
    """脚本主流程"""
    print("🚀 开始每日SEO更新流程...")
    print(f"📁 工作目录: {SITE_ROOT}")
    
    # 1. 生成新文章数据
    print("\n📝 生成新文章数据...")
    文章数据 = 生成文章数据()
    print(f"   - 标题: {文章数据['标题']}")
    print(f"   - 文件名: {文章数据['文件名']}")
    print(f"   - 日期: {文章数据['日期']}")
    
    # 2. 检查重复
    print("\n🔍 检查重复文章...")
    if 检查重复文章(文章数据["标题"]):
        print("⚠️  发现重复文章，跳过生成")
        return False
    print("✅ 无重复文章")
    
    # 3. 生成文章HTML文件
    print("\n📄 生成文章HTML文件...")
    文章HTML = 生成文章HTML模板(文章数据)
    文章文件路径 = ARTICLES_DIR / f"{文章数据['文件名']}.html"
    
    try:
        with open(文章文件路径, 'w', encoding='utf-8') as f:
            f.write(文章HTML)
        print(f"✅ 文章文件已创建: {文章文件路径.name}")
        print(f"   - 文件大小: {len(文章HTML)} 字节")
    except Exception as e:
        print(f"❌ 创建文章文件失败: {e}")
        return False
    
    # 4. 生成首页卡片
    print("\n🏠 生成首页文章卡片...")
    首页卡片 = 生成首页文章卡片(文章数据)
    print("✅ 首页卡片生成完成")
    
    # 5. 更新首页
    print("\n🔄 更新首页精选内容...")
    if not 更新首页精选内容(首页卡片):
        print("❌ 更新首页失败")
        return False
    
    # 6. 更新sitemap
    print("\n🗺️  更新sitemap.xml...")
    if not 更新sitemap(文章数据["URL"]):
        print("❌ 更新sitemap失败")
        return False
    
    # 7. 推送GitHub
    print("\n📤 推送更新到GitHub...")
    if not 推送GitHub():
        print("❌ GitHub推送失败")
        return False
    
    print("\n" + "="*50)
    print("✅ 每日SEO更新完成！")
    print("="*50)
    print(f"📊 总结:")
    print(f"   - 新文章: {文章数据['标题']}")
    print(f"   - 文章URL: {文章数据['URL']}")
    print(f"   - 首页位置: 精选内容区域第1位")
    print(f"   - sitemap: 已添加新URL")
    print(f"   - GitHub: 已提交并推送")
    print("="*50)
    
    return True

if __name__ == "__main__":
    try:
        成功 = 主流程()
        exit(0 if 成功 else 1)
    except Exception as e:
        print(f"❌ 脚本执行出错: {e}")
        exit(1)