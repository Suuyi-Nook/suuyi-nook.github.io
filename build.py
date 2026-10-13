"""修改 content.json 后运行 python build.py，生成可直接发布的静态页面。"""
import json
import posixpath
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
categories = {c['slug']: c for c in data['categories']}
pages = []
e = escape

def url(current, target):
    return posixpath.relpath(target, posixpath.dirname(current) or '.')

def link(current, target, label, cls=''):
    return f'<a class="{cls}" href="{url(current, target)}">{label}</a>'

def crumbs(current, items):
    links = [link(current, 'index.html', '首页')]
    for title, path in items:
        links.append(link(current, path, e(title)) if path else f'<b aria-current="page">{e(title)}</b>')
    return '<nav class="crumbs" aria-label="面包屑">' + '<span aria-hidden="true">/</span>'.join(links) + '</nav>'

def layout(path, title, body, section='home', description=None, noindex=False):
    nav = ''
    for i, (key, name, target) in enumerate([('home','首页','index.html'),('about','关于','about/index.html'),('projects','项目','projects/index.html')],1):
        active = ' aria-current="page"' if section == key else ''
        nav += f'<a href="{url(path,target)}"{active}><span>0{i}</span>{name}</a>'
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · Suuyi’s Nook</title><meta name="description" content="{e(description or data['tagline'])}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="icon" type="image/svg+xml" href="{url(path,'assets/favicon.svg')}"><link rel="stylesheet" href="{url(path,'assets/site.css')}">
<script src="{url(path,'assets/site.js')}" defer></script></head><body id="top"><a class="skip" href="#main">跳到主要内容</a>
<div class="shell"><aside class="rail"><a class="seal" href="{url(path,'index.html')}" aria-label="素衣，返回首页">素</a><p class="rail-label">A SMALL PLACE<br>FOR GROWING IDEAS.</p><nav class="nav" aria-label="主要导航">{nav}</nav><div class="rail-end"><button class="theme" data-theme-toggle type="button">昼 / 夜</button><p>EST. 2026<br>SUUYI’S NOOK</p></div></aside>
<div class="page"><header class="masthead"><a class="wordmark" href="{url(path,'index.html')}">Suuyi’s Nook</a><div class="micro">素衣的小站<br>PHYSICS · COMPUTATION</div></header>
<main id="main">{body}</main><footer class="footer"><span>© 2026 素衣 · 留下理解形成的过程</span><span><a href="{e(data['github'])}">GitHub ↗</a>　 /　 <a href="#top">回到页首 ↑</a></span></footer></div></div></body></html>'''
    out = ROOT / path
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(html,encoding='utf-8')
    pages.append(path)

def hero(kicker, title, description):
    return f'<section class="hero"><p class="kicker">{kicker}</p><h1>{title}</h1><p class="lead">{description}</p></section>'

def category_grid(path):
    rows = ''
    for i,c in enumerate(data['categories'],1):
        count = sum(p['category'] == c['slug'] for p in data['projects'])
        rows += f'''<a class="category" href="{url(path,'projects/'+c['slug']+'/index.html')}"><span class="num">0{i} / {e(c['en'])}</span><h3>{e(c['name'])}</h3><p>{e(c['description'])}</p><div class="tail"><span>{str(count)+' 个项目' if count else '等待第一份作品'}</span><span aria-hidden="true">↗</span></div></a>'''
    return '<div class="category-grid">'+rows+'</div>'

def project_rows(path, projects):
    rows = ''
    for p in projects:
        rows += f'''<article class="project-row"><div class="year">{e(p['year'])}</div><div><h3>{link(path,'projects/'+p['category']+'/'+p['slug']+'/index.html',e(p['title'])+' ↗')}</h3><p>{e(p['summary'])}</p><div>{''.join('<span class="tag">'+e(t)+'</span>' for t in p['tags'])}</div></div><div class="status">{e(p['status'])}</div></article>'''
    return rows

path='index.html'
body=f'''<section class="hero"><div class="hero-grid"><div><p class="kicker">01 / A PERSONAL CORNER</p><h1>在物理与计算之间，<br>持续建立<br>自己的理解。</h1><p class="lead">{e(data['intro'])}</p><div class="actions">{link(path,'projects/index.html','浏览项目 ↗','button primary')}{link(path,'about/index.html','认识素衣','button')}</div></div><div class="map"><div class="map-title">A PLACE TO BEGIN</div><div class="map-root">Ideas, taking shape.</div><div class="map-branch"><div class="map-row">{link(path,'about/index.html','01　个人介绍')}<small>About</small></div><div class="map-row">{link(path,'projects/index.html','02　项目展示')}<small>Projects</small></div><div class="map-row"><span>　分类 → 项目 → 过程</span><small>Explore</small></div></div><div class="map-footer">慢慢探索，慢慢成形。</div></div></div></section>
<section class="section"><div class="section-top"><div><p class="kicker">02 / COLLECTIONS</p><h2>从这里开始探索</h2></div>{link(path,'projects/index.html','全部项目 →','text-link')}</div>{category_grid(path)}</section>
<section class="section"><div class="section-top"><div><p class="kicker">03 / IN THE MAKING</p><h2>第一份作品，从这里开始</h2></div></div>{project_rows(path,data['projects'])}</section>
<section class="section split"><p class="kicker">A NOTE TO VISITORS</p><div><h3>内容慢慢来，结构先清楚。</h3><p>小站刚刚开始整理。目前公开个人介绍与项目展示，更多作品会在准备好之后加入。欢迎从一个项目出发，看看它如何成形。</p>{link(path,'about/index.html','关于这个小站 →','text-link')}</div></section>'''
layout(path,'首页',body)

path='about/index.html'
body=crumbs(path,[('关于',None)])+hero('ABOUT / 个人介绍','你好，我是素衣。',e(data['about']))
body+=f'''<section class="section split"><p class="kicker">01 / INTERESTS</p><div><h2>在问题与实现之间</h2><p>关注物理问题，也关注计算如何帮助理解问题。希望把探索中的想法整理成清楚、可回看、可复用的作品。</p></div></section><section class="section split"><p class="kicker">02 / THIS SPACE</p><div><h2>一个逐渐生长的小站</h2><p>这里先从个人介绍与项目展示开始。项目按研究实践、科学计算、网页与工具分类，每个项目有独立页面，记录背景、方法和进展。</p><p>更具体的经历与成果正在整理中。</p>{link(path,'projects/index.html','前往项目展示 →','text-link')}</div></section><section class="section split"><p class="kicker">03 / ELSEWHERE</p><div><h2>在 GitHub 找到我</h2><a class="button" href="{e(data['github'])}">@Suuyi-Nook ↗</a></div></section>'''
layout(path,'关于素衣',body,'about')

path='projects/index.html'
body=crumbs(path,[('项目',None)])+hero('PROJECTS / 项目展示','让想法有迹可循。','按方向浏览作品，再走进每个项目的背景、方法与进展。')
body+='<section class="section">'+category_grid(path)+'</section><section class="section"><h2>所有项目</h2>'+project_rows(path,data['projects'])+'</section>'
layout(path,'项目展示',body,'projects')

for c in data['categories']:
    path='projects/'+c['slug']+'/index.html'
    selected=[p for p in data['projects'] if p['category']==c['slug']]
    body=crumbs(path,[('项目','projects/index.html'),(c['name'],None)])+hero(e(c['en'])+' / 项目分类',e(c['name']),e(c['description']))
    body+='<section class="section">'
    if selected:
        body+=project_rows(path,selected)
    else:
        body+='<div class="empty"><p class="kicker">A LITTLE ROOM TO GROW</p><h2>第一份作品，还在路上。</h2><p>这个分类暂时没有公开项目。整理完成后，会在这里展示项目简介，并提供详细过程。</p>'+link(path,'projects/index.html','看看其他项目 →','text-link')+'</div>'
    body+='</section>'
    layout(path,c['name'],body,'projects')

for p in data['projects']:
    c=categories[p['category']]
    path='projects/'+c['slug']+'/'+p['slug']+'/index.html'
    body=crumbs(path,[('项目','projects/index.html'),(c['name'],'projects/'+c['slug']+'/index.html'),(p['subtitle'],None)])
    body+=hero(e(p['subtitle']),e(p['title']),e(p['summary']))
    body+='<div class="section detail-meta"><span>'+e(p['year'])+'</span><span>'+e(p['status'])+'</span><span>'+e(' / '.join(p['tags']))+'</span></div>'
    body+='<div class="article"><div>'+''.join(f'<section id="part-{i}"><p class="kicker">0{i}</p><h2>{e(s["title"])}</h2><p>{e(s["body"])}</p></section>' for i,s in enumerate(p['sections'],1))+'</div>'
    body+='<nav class="toc" aria-label="本页目录"><p class="kicker">ON THIS PAGE</p>'+''.join(f'<a href="#part-{i}">0{i}　{e(s["title"])}</a>' for i,s in enumerate(p['sections'],1))+'</nav></div>'
    body+='<section class="section">'+link(path,'projects/'+c['slug']+'/index.html','← 返回'+e(c['name']),'text-link')+'</section>'
    layout(path,p['title'],body,'projects')

# 404 is served for arbitrary URL depths, so its shared assets and routes are root-relative.
layout('404.html','页面未找到',hero('404 / NOT FOUND','这条小径还没有铺好。','页面可能已经移动，也可能尚未发布。')+'<section class="section"><a href="/" class="button primary">回到首页</a></section>',noindex=True)
error=(ROOT/'404.html').read_text(encoding='utf-8')
for target in ['assets/favicon.svg','assets/site.css','assets/site.js','index.html','about/index.html','projects/index.html']:
    error=error.replace('"'+target+'"','"/'+target+'"')
(ROOT/'404.html').write_text(error,encoding='utf-8')
print(f'Generated {len(pages)} pages.')
