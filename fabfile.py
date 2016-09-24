# -*- coding: utf-8 -*-

import os
import yaml

from fabric.api import env, local, run, lcd,  cd, sudo, warn_only, prompt
from fabric.contrib.console import confirm

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"


def stripped(parts):
	ret = []
	for p in parts:
		s = p.replace("\t", "")
		s = s.strip()
		if len(s) == 0:
			ret.append(None)
		else:
			ret.append(s)
	return ret
		
	


def imp():
	
	a2z = {}
	
	
	with open("Raw.txt", "r") as f:
		contents = f.read()
		
		lines = contents.split("\n")
		
		for raw_line in lines:
			line = raw_line.strip()
			if "–" in line:
				parts = line.split("–")
				if len(parts) > 1:
					# strp
					sparts =  stripped(parts)				
					print sparts
					term = sparts[0]
					az = sparts[0][0].lower()
					if not az in a2z:
						a2z[az] = {}
					
					defs = sparts[1:]
					a2z[az] [term] = dict(defs=defs)
					
				else:
					#print "  ??:", parts
					pass
			else:
				#print "   ?:", line
				pass
	print a2z.keys()		
	## Now we serialse to yaml

	for a_char in a2z:
		dir_path = ROOT + a_char
		print "=",  dir_path
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		data = a2z[a_char]
		yaml_str = yaml.dumps(data)
		file_name = a.replace(" ", "_") + ".yaml"
		print file_name 
					
		