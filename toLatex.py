import yaml
import re


cv = yaml.safe_load(open('cv.yaml', 'r'))
texFile = open('tex/template.tex','r')
tex = texFile.read()
texFile.close()

tex = re.sub('\$FIRSTNAME',cv['first name'],tex)
tex = re.sub('\$LASTNAME',cv['last name'],tex)

texFile = open('tex/main.tex','w')
texFile.write(tex)
texFile.close()

