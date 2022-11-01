import functools
import yaml
import regex as re
import sys

CV_YAML      = 'cv.yaml'
TEMPLATE_TEX = 'tex/template.tex'
MAIN_TEX     = 'tex/moderncv/main.tex'

RENDER = {
        'en' : True,
        'sv' : False,
        'no' : False
}

TEXBR = '\\\\\n'

def parseLanguageArgs():
    global RENDER
    for arg in sys.argv:
        if arg not in RENDER.keys() and arg != 'toLatex.py':
            print('Invalid language code')
            exit(1)
        elif arg != 'toLatex.py':
            RENDER[arg] = True

def load():
    with open(CV_YAML, 'r') as f:
        CV = yaml.safe_load(f)
    with open(TEMPLATE_TEX,'r') as f:
        TEX = f.read()
    return CV, TEX

def sub(var, tex, cv):
    templateVar = '\${}'.format(var.upper())
    return re.sub(templateVar, cv[var], tex)

def sub_lang(tex, var=None, cv=None, lang=None):
    lvar = '\${}-{}'.format(var.upper(), lang.upper())
    lsub = cv['{}-{}'.format(var,lang)] if RENDER[lang] else ''
    return re.sub(lvar, lsub, tex)

def sub_multilang(var, tex, cv):
    funcList = [
                functools.partial(sub_lang, var=var, cv=cv, lang=l)
                for l in cv['languages']
            ]
    return functools.reduce(lambda t, f: f(t), funcList, tex)

def write(tex):
    texFile = open(MAIN_TEX,'w')
    texFile.write(tex)
    texFile.close()


def mdToTex(md, i=0, nitems=0):
    # Bold
    tex = re.sub(r"\*\*([^\*]*)\*\*", r"\\textbf{\1}", md)
   # Ampersands
    tex = tex.replace("&","\&")
    # Newlines
    tex = tex.replace("\n",TEXBR)
    # Links
    linkPattern = re.compile(r'\[([^][]+)\](\(((?:[^()]+|(?2))+)\))')
    for match in linkPattern.finditer(tex):
        text, _, url = match.groups()
        # Fix for accidentally interpreting underscores as italics
        newUrl = str(url).replace('_','\\%5F')
        tex = tex.replace(f'[{text}]({url})', texCmd('href', [newUrl,text]))

    # Italics
    tex = re.sub(r"\_([^\*]*)\_", r"\\textit{\1}", tex)

    # Make a list
    bullet = "\\item[$\\usym{2727}$]"
    if i == 1:
        tex = '\\begin{itemize}' + bullet + tex
    elif i > 1:
        tex = ' ' + bullet + tex
    if i != 0 and i == nitems - 1:
        tex = tex + '\\end{itemize}\\vspace*{-\\baselineskip}\\leavevmode'

    return tex

def texCmd(name, args):
    return '\\' + name + ''.join(['{'+a+'}' for a in args])

def pagebreak(section, cv):
    return '\\newpage \n' if section in cv['tex-pagebreaks'] else ''

def section(name,sub):
    return texCmd('subsection' if sub else 'section', [name])

def cvitem(when, what):
    return texCmd('cvitem', [when,what])

def makeSectionTex(sec, cv, sub=False):
    sectionTex = pagebreak(sec,cv) + section(sec,sub) + '\n' + '\n'.join([
        cvitem(mdToTex(item['when']), TEXBR.join([
                mdToTex(line,i, len(item['what'])) for i,line in enumerate(item['what'])
            ])) for item in cv[sec]
    ])
    subsecsTex = ''.join(
            ''.join(
                [makeSectionTex(ss,cv,sub=True) for ss in cv['subsections'][sec]]
            )
            if sec in cv['subsections'].keys() else ''
            )
    return sectionTex + subsecsTex


def makeSections(tex, cv):
    sectionsTex = '\n'.join([makeSectionTex(s, cv) for s in cv['sections']])
    tex = tex.replace('$SECTIONS',sectionsTex)
    return tex

def addLinks(tex, cv):
    texLink = lambda url,txt:'\\href{'+url+'}{\\underline{'+txt+'}}\n\\\\\n'
    linkTex = ''.join([texLink(l['url'],l['txt']) for l in cv['links']])
    tex     = tex.replace('$LINKS', linkTex)
    tex     = tex.replace('$PICTURE', cv['picture'])
    return tex

def makeHeader(tex, cv):
    tex = sub('firstname', tex, cv)
    tex = sub('lastname', tex, cv)
    tex = sub_multilang('pronouns', tex, cv)
    tex = addLinks(tex, cv)
    return tex
 
def main():
    parseLanguageArgs()
    cv, tex = load()
    tex = makeHeader(tex, cv)
    tex = makeSections(tex, cv)
    write(tex)

if __name__ == '__main__':
    main()
