# -*- coding: utf-8 -*-

import os
import json
import yaml
from string import Template

from fabric.api import env, local, run, lcd,  cd, sudo, warn_only, prompt
from fabric.contrib.console import confirm

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"

GLOSS_DIR = os.path.join(ROOT, "yoga_glossary")


def _read_yaml(file_path):
	print file_path
	with open(file_path, 'r') as stream:
		try:
			return yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)

_template = Template( """
<tr>
	<td><b>$term</b></td>
	<td>$definition</td>
</tr>
""")

def yg_build():
	
	#dic = {}
	lst = []
	html_gloss = ""
	
	## need to yaml from all subs, and knock out
	a2z_dirs = os.listdir(GLOSS_DIR)
	for az_dir in sorted(a2z_dirs, key=str.lower):   
		
		yaml_files =  os.listdir(os.path.join(GLOSS_DIR, az_dir))
		for yfile in sorted(yaml_files, key=str.lower):
			print "------------"
			data = _read_yaml(os.path.join(GLOSS_DIR, az_dir, yfile))
			
			print data['term']
			lst.append(data)
			def_li = " ".join(["<li>%s</li>" % d for d in data['definition']])
			def_li = "<ul>" + def_li + "</ul>"
			#print def_li
			#print _template.substitute(term=data['term'], definition=def_li)
			html_gloss += _template.substitute(term=data['term'], definition="<ul>" + def_li + "</ul>")
			
			#dic[data['term']] = data['definition']
	
	with open(os.path.join(ROOT, "bits", "template.html"), "r") as f:
		tpl_contents = f.read()
		f.close
		tpl_contents = tpl_contents.replace("###GLOSSARY_CONTENT###", html_gloss)
		with open(os.path.join(ROOT, "docs", "index.html"), "w") as f:
			f.write( tpl_contents )
			f.close()
				
	with open(os.path.join(ROOT, "docs", "yoga-glossary.json"), "w") as f:
			f.write( json.dumps( lst, sort_keys=True, indent=4, separators=(',', ': ')) )
			f.close()
	with open(os.path.join(ROOT, "docs", "yoga-glossary-min.json"), "w") as f:
			f.write( json.dumps( lst  ) )
			f.close()          
			
	local("cp %sdocs/yoga-glossary-min.json /home/padma/yoga-glossary-android/app/src/main/assets/yoga-glossary.json" % ROOT)
			
		