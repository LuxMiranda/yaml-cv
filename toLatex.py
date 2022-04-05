import yaml
import re

CV_YAML      = 'cv.yaml'
TEMPLATE_TEX = 'tex/template.tex'
MAIN_TEX     = 'tex/main.tex'

RENDER = {
        'en' : True,
        'sv' : True,
        'no' : True
}

def load():
    with open(CV_YAML, 'r') as f:
        CV = yaml.safe_load(f)
    with open(TEMPLATE_TEX,'r') as f:
        TEX = f.read()
    return CV, TEX

def sub(var, tex, cv):
    templateVar = '\${}'.format(var.upper())
    return re.sub(templateVar, cv[var], tex)

def langSub(var, tex, cv):
    for lang in cv['languages']:
        lvar = '\${}-{}'.format(var.upper(), lang.upper())
        lsub = '({})'.format(cv['{}-{}'.format(var,lang)]) if RENDER[lang] else ''
        tex = re.sub(lvar, lsub, tex)
    return tex


def write(tex):
    texFile = open(MAIN_TEX,'w')
    texFile.write(tex)
    texFile.close()

def main():
    cv, tex = load()
    tex = sub('firstname', tex, cv)
    tex = sub('lastname', tex, cv)
    tex = langSub('pronouns', tex, cv)
    write(tex)


if __name__ == '__main__':
    main()
