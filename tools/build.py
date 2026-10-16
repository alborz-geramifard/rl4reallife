"""Render 2019..2022.html and index.html from data/rl4reallife.json."""
import json, html, os, re, hashlib
ROOT=os.path.join(os.path.dirname(__file__),'..')
D=json.load(open(os.path.join(ROOT,'data','rl4reallife.json')))
CSSV=hashlib.md5(open(os.path.join(ROOT,'assets','style.css'),'rb').read()).hexdigest()[:8]
e=html.escape
YEARS=['2022','2021','2020','2019']
ORIG={'2022':'https://sites.google.com/view/RL4RealLife','2021':'https://sites.google.com/view/RL4RealLife2021','2020':'https://sites.google.com/view/RL4RealLife2020','2019':'https://sites.google.com/view/RL4RealLife2019'}
I_CAL='<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>'
I_PIN='<svg viewBox="0 0 24 24"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>'
I_DOC='<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>'
def a(u,t,cls=''):
    c=(' class="%s"'%cls) if cls else ''; ext='' if u.endswith('.html') else ' target="_blank" rel="noopener"'
    return '<a%s href="%s"%s>%s</a>'%(c,e(u),ext,t)
def person(p):
    name=a(p['url'],e(p['name'])) if p.get('url') else e(p['name'])
    ini=''.join(w[0] for w in re.sub(r'\(.*?\)','',p['name']).replace('-',' ').split()[:2]).upper()
    pic=f'<img class="face" src="{e(p["photo"])}" alt="" loading="lazy">' if p.get('photo') else f'<span class="face ini">{e(ini)}</span>'
    role=f'<em class="role">{e(p["role"])}</em>' if p.get('role') else ''
    extra=' '.join(a(u,e(t)+' ↗','mini') for t,u in p.get('links',[]))
    extra_html=('<span class="mini-row">'+extra+'</span>') if extra else ''
    return f'<div class="person">{pic}<div><b>{name}</b>{role}<span>{e(p.get("aff") or "")}</span>{extra_html}</div></div>'
def rail(cur):
    out=[]
    for y in YEARS:
        d=D[y]; on=' class="on"' if y==cur else ''
        out.append(f'<li{on}><a href="{y}.html"><span class="dot"></span><span><span class="y">{y}</span><br><span class="w">{e(d["conf"].replace("Virtual","Virtual workshop"))}<br>{e(d["city"].split(",")[0])}</span></span></a></li>')
    return '<ol>'+''.join(out)+'</ol>'
def paper(p):
    btns=''.join(a(u,(I_DOC+' ' if t=='paper' else '')+e(t.capitalize()),'pdf' if t=='paper' else 'pdf alt') for t,u in p['links'])
    note=f'<span class="note-tag">{e(p["note"])}</span>' if p.get('note') else ''
    return f'<li><div><div class="pt">{e(p["title"])}{note}</div><div class="pa">{e(p["authors"])}</div></div><div class="btns">{btns}</div></li>'
def sched(items):
    out=[]
    for it in items:
        links=''.join(a(u,e(t.capitalize())+' ↗') for t,u in it['links'])
        if not it['time']: out.append(f'<li class="sess">{it["what"]}</li>'); continue
        cls=' class="brk"' if it['brk'] else ''
        out.append(f'<li{cls}><span class="t">{e(it["time"])}</span><span>{it["what"]}<span class="l">{links}</span></span></li>')
    return '<ul class="sched">'+''.join(out)+'</ul>'
def page(y):
    d=D[y]
    intro=''.join(f'<p>{p}</p>' for p in d['intro'])
    top=''.join(a(u,e(t)+' ↗','chip') for t,u in d.get('top_links',[]) if u)
    talks=''
    for t in d['talks']:
        pic=f'<img class="face big" src="{e(t["photo"])}" alt="">' if t.get('photo') else ''
        vid=a(t['video'],'Video ↗','mini') if t.get('video') else ''
        aff=(' · '+e(t['aff'])) if t.get('aff') else ''; ab=('<p class="ab">'+t['abstract']+'</p>') if t.get('abstract') else ''; bio=('<p class="bio"><b>Bio.</b> '+t['bio']+'</p>') if t.get('bio') else ''
        talks+=f'<article class="talk">{pic}<div><div class="tk">{e(t["name"])}{aff}</div><h3>{e(t["title"])}</h3>{ab}{bio}{vid}</div></article>'
    panels=''
    for p in d['panels']:
        hdr=' · '.join(x for x in [e(p.get('when','')), e(p.get('chairs',''))] if x)
        tools=' '.join(x for x in [a(p['video'],'Video ↗','mini') if p.get('video') else '', a(p['ask'],'Audience questions ↗','mini') if p.get('ask') else ''] if x)
        h1=('<div class="ph">'+hdr+'</div>') if hdr else ''; h2=('<div class="ph">'+tools+'</div>') if tools else ''; mem=''.join(person(m) for m in p['members'])
        panels+=f'<div class="panel"><h3>{e(p["name"])}</h3>{h1}{h2}<div class="people">{mem}</div></div>'
    pintro=f'<p class="muted">{d["panels_intro"]}</p>' if d.get('panels_intro') else ''
    papers=''
    for g in d['paper_groups']:
        papers+=(f'<div class="sub">{e(g["title"])}</div>' if len(d['paper_groups'])>1 else '')+'<ol class="papers">'+''.join(paper(p) for p in g['papers'])+'</ol>'
    npap=sum(len(g['papers']) for g in d['paper_groups'])
    pap_intro=f'<p class="muted">{d["papers_intro"]}</p>' if d.get('papers_intro') else ''
    specs=f'<p class="note">{d["poster_specs"]}</p>' if d.get('poster_specs') else ''
    cfp=''.join(f'<p>{x}</p>' for x in d['cfp'])+''.join(f'<p class="small">{x}</p>' for x in d.get('cfp_extra',[]))
    dates=''.join(f'<div><div class="dl">{e(l)}</div><div class="dv">{v}</div></div>' for l,v in d['dates'])
    cfpanels=('<div class="sub">Call for panels</div><div class="card desc">'+''.join('<p>%s</p>'%x for x in d['call_for_panels'])+'</div>') if d.get('call_for_panels') else ''
    chairs=''.join(person(p) for p in d['chairs'])
    guest=('<div class="sub">'+e(d['guest_editors_label'])+'</div><div class="people">'+''.join(person(p) for p in d['guest_editors'])+'</div>') if d.get('guest_editors') else ''
    pc=''.join(f'<div>{e(x)}</div>' for x in d['pc'])
    comm=''.join((a(u,e(t)) if u else e(t)) for t,u in d.get('comm',[]))
    comm='<div class="chips">'+''.join((a(u,e(t)+' ↗','chip') if u else '<span class="chip">%s</span>'%e(t)) for t,u in d.get('comm',[]))+'</div>'
    prev=''.join(f'<li>{a(u,e(t))}</li>' for t,u in d.get('previous',[]))
    stats=''.join(f'<span>{e(s)}</span>' for s in [f'{npap} papers', f'{len(d["talks"])} invited talks' if d['talks'] else '', f'{len(d["panels"])} panel{"s" if len(d["panels"])>1 else ""}' if d['panels'] else '', e(d['mode'])] if s)
    vc=d.get('venue_credit') or {}
    credit=a(vc['page'],f'Photo: {e(vc["artist"][:40])} ({e(vc["license"])})','credit') if vc.get('artist') else ''
    loc=a(d['location_url'],e(d['location'])) if d.get('location_url') else e(d['location'])
    top=a(ORIG[y],'Original website ↗','chip orig')+top
    top_html='<div class="chips">'+top+'</div>'
    talks_sec=('<section id="talks"><div class="eyebrow">Invited</div><h2>Invited talks</h2><div class="talks">'+talks+'</div></section>') if talks else ''
    panels_sec=('<section id="panels"><div class="eyebrow">Discussion</div><h2>Panels</h2>'+pintro+panels+'</section>') if panels else ''
    pc_sec=('<section id="committee"><div class="eyebrow">Reviewers</div><h2>Program committee</h2><div class="pc">'+pc+'</div></section>') if pc else ''
    prev_html=''
    city_html=(', '+e(d['city'])) if d['city']!='Online' else ''
    tabs=['<a href="#overview">Overview</a>','<a href="#schedule">Schedule</a>']+(['<a href="#talks">Invited talks</a>'] if d['talks'] else [])+(['<a href="#panels">Panels</a>'] if d['panels'] else [])+['<a href="#papers">Accepted papers</a>','<a href="#cfp">Call for papers</a>','<a href="#organizers">Organizers</a>']+(['<a href="#committee">Program committee</a>'] if d['pc'] else [])+['<a href="#links">Links</a>']
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>RL for Real Life · {e(d['conf'])}</title>
<meta name="description" content="Reinforcement Learning for Real Life workshop, {e(d['conf'])}: schedule, talks, panels, accepted papers and organizers.">
<link rel="icon" href="assets/logo.png">
<link rel="canonical" href="https://alborz-geramifard.com/rl4reallife/{y}.html">
<meta property="og:type" content="website"><meta property="og:site_name" content="Reinforcement Learning for Real Life">
<meta property="og:title" content="RL for Real Life · {e(d['conf'])}"><meta property="og:description" content="Reinforcement Learning for Real Life workshop, {e(d['conf'])}: schedule, talks, panels, accepted papers and organizers.">
<meta property="og:url" content="https://alborz-geramifard.com/rl4reallife/{y}.html"><meta property="og:image" content="https://alborz-geramifard.com/rl4reallife/{e(d['venue_image'])}">
<meta name="twitter:card" content="summary_large_image">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-N1V1ZB8K1T"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-N1V1ZB8K1T');</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css?v={CSSV}">
</head>
<body>
<header class="banner"><div class="in"><img src="assets/logo.png" alt=""><div class="t">Reinforcement Learning for Real Life <span class="rl2">(RL<sup>2</sup>)</span></div></div></header>
<div class="layout">
  <aside class="rail">{rail(y)}</aside>
  <main class="main">
    <div class="hero photo" style="background-image:url('{e(d['venue_image'])}');background-position:{e(d.get('venue_focus','center'))}">
      {credit}
      <div class="k">{e(d['conf'])} workshop · {e(d['edition'])} edition</div>
      <h1>Reinforcement Learning for Real Life</h1>
      <div class="meta"><span>{I_CAL}{e(d['date'])}</span><span>{I_PIN}{loc}{city_html}</span></div>
      <div class="stats">{stats}</div>
    </div>
    <nav class="tabs">{''.join(tabs)}</nav>
    <section id="overview"><div class="eyebrow">Overview</div><h2>About the workshop</h2><div class="card desc">{intro}</div>{top_html}</section>
    <section id="schedule"><div class="eyebrow">Program</div><h2>Schedule</h2>{sched(d['schedule'])}</section>
    {talks_sec}
    {panels_sec}
    <section id="papers"><div class="eyebrow">Contributed</div><h2>Accepted papers</h2>{pap_intro}{specs}{papers}</section>
    <section id="cfp"><div class="eyebrow">Archive</div><h2>Call for papers</h2><div class="card desc">{cfp}</div><div class="sub">Important dates</div><div class="dates">{dates}</div>{cfpanels}</section>
    <section id="organizers"><div class="eyebrow">People</div><h2>Organizers</h2><div class="sub">Co-chairs</div><div class="people">{chairs}</div>{guest}</section>
    {pc_sec}
    <section id="links"><div class="eyebrow">More</div><h2>Links</h2>{comm}{prev_html}</section>
  </main>
</div>
<footer>Reinforcement Learning for Real Life workshop series, 2019 – 2022 · Archived from the <a href="{ORIG[y]}" target="_blank" rel="noopener">original {y} website</a></footer>
</body>
</html>'''
for y in YEARS: open(os.path.join(ROOT,f'{y}.html'),'w').write(page(y))
open(os.path.join(ROOT,'index.html'),'w').write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=2022.html"><title>RL for Real Life</title><a href="2022.html">RL for Real Life workshop series</a>')
print('built',YEARS)
