import yaml
import regex as re

CV_YAML  = 'cv.yaml'
TEMPLATE = 'html/template.md'
OUTPUT   = 'html/cv.md'
BR = '<br>'

def load():
    with open(CV_YAML, 'r') as f:
        CV = yaml.safe_load(f)
    with open(TEMPLATE, 'r') as f:
        HTML = f.read()
    return CV, HTML

def section(name,sub):
    line = '' if sub else '<img class="gradient" src="/images/gradient.png" />'
    headerclass = 'cvsubheader' if sub else 'cvheader'
    rowclass = 'cvsubheaderrow' if sub else 'cvheaderrow'
    idname = name.lower().replace(' ','-')
    return f"""
        <tr class="{rowclass}" id="{idname}">
            <td class="{headerclass}">{line}</td>
            <td class="{headerclass}">{name}</td>
        </tr>
    """


def cvitem(when, what):
    return f"""
        <tr>
            <td>{when}</td>
            <td>{what}</td>
        </tr>
    """

def link(url, text):
    return f'<a href="{url}"><strong>{text}</strong></a>'

def mdToTex(md,i=0,nitems=0):
    # Bold
    tex = re.sub(r"\*\*([^\*]*)\*\*", r"<strong>\1</strong>", md)
    # Ampersands
    #tex = tex.replace("&","\&")
    # Newlines
    tex = tex.replace("\n",BR)
    # Links
    linkPattern = re.compile(r'\[([^][]+)\](\(((?:[^()]+|(?2))+)\))')
    for match in linkPattern.finditer(tex):
        text, _, url = match.groups()
        newUrl = str(url).replace('_','%5F')
        tex = tex.replace(f'[{text}]({url})', link(newUrl,text))

    # Italics
    tex = re.sub(r"\_([^\*]*)\_", r"<i>\1</i>", tex)

    # Currency amounts
    currency_cmds = re.findall(r'CurrencyUSD\([0-9]*\)', tex)
    for cmd in currency_cmds:
        amount = int(cmd[12:-1])
        formatted_amount = '${:,} USD'.format(amount)
        tex = tex.replace(cmd, formatted_amount)

    # Make a list
    if i == 1:
        tex = '<ul><li>' + tex + '</li>'
    elif i > 1:
        tex = '<li>' + tex + '</li>'
    if i != 0 and i == nitems - 1:
        tex = tex + '</ul>'
    return tex


def makeSectionTex(sec, cv, sub=False):
    sectionTex = section(sec,sub) + '\n' + '\n'.join([
        cvitem(mdToTex(item['when']), BR.join([
                mdToTex(line,i,len(item['what'])) for i,line in enumerate(item['what'])
            ])) for item in cv[sec]
    ])
    subsecsTex = ''.join(
            ''.join(
                [makeSectionTex(ss,cv,sub=True) for ss in cv['subsections'][sec]]
            )
            if sec in cv['subsections'].keys() else ''
            )
    sectionid = sec.lower().replace(' ','-')
    return sectionTex + subsecsTex


def makeSections(cv):
    return '\n'.join([makeSectionTex(s, cv) for s in cv['sections']])

def makeTocNav(cv):
    litems = '\n'.join([
        '<li><a href="#' + s.lower().replace(' ','-') + '">' + s + '</a></li>' for s in cv['sections']
        ])
    return f"""
    <div class="section-nav">
        <ol>
            {litems}
        </ol>
    </div>
    """

def write(html):
    texFile = open(OUTPUT,'w')
    texFile.write(html)
    texFile.close()

def main():
    cv, html = load()
    sections = makeSections(cv)
    tocNav   = makeTocNav(cv)
    html = html.replace('$SECTIONS',sections + tocNav)
    write(html)

if __name__ == '__main__':
    main()
