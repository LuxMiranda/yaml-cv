import functools
import yaml
import re
import sys

CV_YAML      = 'cv.yaml'
TEMPLATE_TEX = 'tex/template.tex'
MAIN_TEX     = 'tex/main.tex'

RENDER = {
        'en' : True,
        'sv' : False,
        'no' : False
}

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
    lsub = '({})'.format(cv['{}-{}'.format(var,lang)]) if RENDER[lang] else ''
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

def makeSections(tex, cv):
    return tex

def addLinks(tex, cv):
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
