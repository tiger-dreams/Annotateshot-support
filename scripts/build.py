#!/usr/bin/env python3
"""Build multilingual support documents and static GitHub Pages. Python 3 only."""
import html,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'content/locales.json').read_text())
SITE='https://tiger-dreams.github.io/Annotateshot-support'
REPO='https://github.com/tiger-dreams/Annotateshot-support'
STORE='https://apps.apple.com/app/annotateshot/id6790591845?mt=12'
SUPPORT='https://annotateshot.com/mac/support'
POLICY='https://annotateshot.com/mac/privacy'
GITHUB_PRIVACY='https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'
REFUND='https://reportaproblem.apple.com/'
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n')
def e(s):return html.escape(s,quote=True)
def issue(kind,lang):
 suffix='' if lang=='en' else '_'+lang
 return REPO+'/issues/new?template='+{'bug':'bug_report','feature':'feature_request','question':'question'}[kind]+suffix+'.yml'
def readme_path(lang):return 'README.md' if lang=='en' else f'README.{lang}.md'
def readme(lang,c):
 nav=' | '.join(f'[{v["name"]}]({readme_path(k)})' for k,v in DATA.items())
 rows='\n'.join(f'| {c[k]} | [{c[k]}]({issue(k,lang)}) |' for k in ['bug','feature','question'])
 return f'''# {c['title']}

{nav}

{c['readme_about']}

**[{c['home']}]({SITE}/{lang}/)** · [{c['store']}]({STORE})

## {c['readme_heading']}

| | |
| --- | --- |
{rows}

[{c['issues']}]({REPO}/issues)

## {c['readme_docs']}

- [{c['guide']}]({SITE}/{lang}/guide.html)
- [{c['faq']}]({SITE}/{lang}/faq.html)
- [{c['privacy']}]({SITE}/{lang}/privacy.html)

{c['public_text']}

{c['private_text']}

[{c['private']}]({SUPPORT}) · [{c['refund']}]({REFUND})

## {c['readme_scope']}

{c['readme_scope_text']}

[{c['policy']}]({POLICY})
'''
def markdown_guide(c):
 steps='\n\n'.join(f'{i}. **{a}** — {b}' for i,(a,b) in enumerate(c['steps'],1))
 items='\n'.join('- '+x for x in c['report_items'])
 return f"# {c['guide']}\n\n{c['guide_intro']}\n\n{steps}\n\n## {c['permission_title']}\n\n{c['permission_text']}\n\n## {c['report_title']}\n\n{items}\n\n{c['public_text']}"
def a(href,text,cls=''):return f'<a href="{e(href)}"'+(f' class="{cls}"' if cls else '')+f'>{e(text)}</a>'
def page(lang,kind,c,root=False):
 prefix='' if root else '../'
 locale_base='en/' if root else './'
 languages=''.join(f'<a href="{prefix}{other}/{kind}.html" lang="{other}" hreflang="{other}"'+(' aria-current="page"' if other==lang else '')+f'>{e(v["name"])}</a>' for other,v in DATA.items())
 nav=''.join(a(locale_base+f'{p}.html',c[key]) for p,key in [('index','home'),('guide','guide'),('faq','faq')])
 cta=a(STORE,c['store'],'button')
 if kind=='index':
  title=c['tagline'];intro=c['intro']
  reports=''.join(f'<a class="request" href="{issue(k,lang)}"><span><strong>{e(c[k])}</strong><span>{e(c[k+"_desc"])}</span></span><span aria-hidden="true">↗</span></a>' for k in ['bug','feature','question'])
  body=f'''<div class="support-layout"><section aria-labelledby="help"><h2 id="help">{e(c['help_title'])}</h2><div class="requests">{reports}</div><p>{a(REPO+'/issues',c['issues'],'text-link')}</p></section><aside class="about"><img src="{prefix}assets/app-icon.png" width="80" height="80" alt=""/><h2>{e(c['about_title'])}</h2><p>{e(c['about_text'])}</p>{a(locale_base+'guide.html',c['guide'],'text-link')}</aside></div><section class="notice"><h2>{e(c['public_title'])}</h2><p>{e(c['public_text'])}</p><p>{e(c['private_text'])}</p><div class="link-row">{a(SUPPORT,c['private'])}{a(REFUND,c['refund'])}</div></section>'''
 elif kind=='guide':
  title=c['guide'];intro=c['guide_intro']
  steps=''.join(f'<li><h2>{e(t)}</h2><p>{e(s)}</p></li>' for t,s in c['steps'])
  body=f'<div class="reading"><ol class="steps">{steps}</ol><section><h2>{e(c["permission_title"])}</h2><p>{e(c["permission_text"])}</p></section><section><h2>{e(c["report_title"])}</h2><ul>'+''.join('<li>'+e(s)+'</li>' for s in c['report_items'])+'</ul>'+a(issue('bug',lang),c['bug'],'button')+'</section></div>'
 elif kind=='faq':
  title=c['faq_title'];intro=c['intro']
  body='<div class="reading faq">'+''.join(f'<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>' for q,ans in c['faqs'])+f'<p class="link-row">{a(issue("question",lang),c["question"])}{a(REFUND,c["refund"])}</p></div>'
 else:
  title=c['privacy'];intro=c['privacy_intro']
  body='<div class="reading">'+''.join(f'<section><h2>{e(t)}</h2><p>{e(s)}</p></section>' for t,s in c['privacy_sections'])+f'<p class="link-row">{a(POLICY,c["policy"])}{a(GITHUB_PRIVACY,c["github_privacy"])}</p></div>'
 canonical=f'{SITE}/{lang}/{kind}.html'
 alternates=''.join(f'<link rel="alternate" hreflang="{k}" href="{SITE}/{k}/{kind}.html">' for k in DATA)
 return f'''<!doctype html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} — Annotateshot</title><meta name="description" content="{e(intro)}"><meta name="theme-color" content="#f3f5f8"><link rel="canonical" href="{canonical}">{alternates}<link rel="icon" href="{prefix}assets/app-icon.png"><link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><a class="skip" href="#main">{e(c['skip'])}</a><div class="shell"><header><a class="brand" href="{locale_base}index.html"><img src="{prefix}assets/app-icon.png" alt="" width="36" height="36"><span>Annotateshot<span>{e(c['home'])}</span></span></a><nav aria-label="{e(c['language'])}" class="languages">{languages}</nav></header><nav class="main-nav" aria-label="{e(c['home'])}">{nav}</nav><main id="main"><div class="hero"><p class="eyebrow">{e(c['title'])}</p><h1>{e(title)}</h1><p class="intro">{e(intro)}</p>{cta}</div>{body}</main><footer><p>{e(c['footer'])}</p><div class="link-row">{a(REPO,c['repo'])}{a(locale_base+'privacy.html',c['privacy'])}{a(SUPPORT,c['private'])}</div></footer></div></body></html>'''

def fields(lang,c,kind):
 body=[{'type':'markdown','attributes':{'value':c['form_notice']}}]
 def field(id,key,required=True,input=False):
  body.append({'type':'input' if input else 'textarea','id':id,'attributes':{'label':c[key]},'validations':{'required':required}})
 if kind=='bug':
  for id,key,input in [('app_version','form_version',True),('macos_version','form_macos',True),('steps','form_steps',False),('expected','form_expected',False),('actual','form_actual',False)]:field(id,key,input=input)
  field('details','form_extra',False)
 elif kind=='feature':
  field('problem','form_problem');field('suggestion','form_suggestion');field('examples','form_examples',False)
 else:
  field('app_version','form_version',False,True);field('question','form_question');field('context','form_context',False)
 return {'name':c[kind]+' · '+c['name'],'description':c[kind+'_desc'],'labels':[{'bug':'bug','feature':'enhancement','question':'question'}[kind],'needs-triage'],'body':body}

def yaml_dump(value,indent=0):
 # JSON-quoted scalars keep punctuation and Unicode valid in YAML without dependencies.
 pad=' '*indent
 if isinstance(value,dict):
  lines=[]
  for k,v in value.items():
   if isinstance(v,(dict,list)):lines.append(pad+k+':\n'+yaml_dump(v,indent+2))
   else:lines.append(pad+k+': '+json.dumps(v,ensure_ascii=False))
  return '\n'.join(lines)
 if isinstance(value,list):
  return '\n'.join(pad+'-\n'+yaml_dump(x,indent+2) if isinstance(x,(dict,list)) else pad+'- '+json.dumps(x,ensure_ascii=False) for x in value)
 raise TypeError(value)

for lang,c in DATA.items():
 assert set(c)==set(DATA['en']),f'Missing translation keys: {lang}'
 write(readme_path(lang),readme(lang,c))
 write(f'docs/{lang}/guide.md',markdown_guide(c))
 for kind in ['index','guide','faq','privacy']:write(f'docs/{lang}/{kind}.html',page(lang,kind,c))
 for kind,filename in [('bug','bug_report'),('feature','feature_request'),('question','question')]:
  suffix='' if lang=='en' else '_'+lang
  write(f'.github/ISSUE_TEMPLATE/{filename}{suffix}.yml',yaml_dump(fields(lang,c,kind)))
write('docs/index.html',page('en','index',DATA['en'],root=True))
write('docs/.nojekyll','')
write('docs/guide.md','# User guides / 사용 안내 / 使い方\n\n'+ '\n'.join(f'- [{c["name"]}]({lang}/guide.md)' for lang,c in DATA.items()))
contrib=[]
for lang,c in DATA.items():
 contrib.append('## '+c['name']+'\n\n'+'\n'.join('- '+s for s in c['contributing'])+'\n\n'+c['readme_scope_text'])
write('CONTRIBUTING.md','# Feedback / 피드백 / フィードバック\n\n'+'\n\n'.join(contrib))
write('.github/ISSUE_TEMPLATE/config.yml',yaml_dump({'blank_issues_enabled':False,'contact_links':[{'name':'Private support · 비공개 지원 · 非公開のお問い合わせ','url':SUPPORT,'about':'Requests involving private information / 개인정보가 필요한 문의 / 個人情報を含むお問い合わせ'},{'name':'App Store refunds · 환불 · 返金','url':REFUND,'about':'Request refunds through Apple / Apple에 환불 요청 / Appleへ返金を申請'}]}))
print('Built 3 localized READMEs, 9 issue forms, and 13 static pages.')
