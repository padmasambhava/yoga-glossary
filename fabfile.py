# -*- coding: utf-8 -*-

import os
import json
import yaml

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

def yg_build():
    
    dic = {}
    lst = []
    
    ## need to yaml from all subs, and knock out
    a2z_dirs = os.listdir(GLOSS_DIR)
    for az_dir in sorted(a2z_dirs, key=str.lower):   
        
        yaml_files =  os.listdir(os.path.join(GLOSS_DIR, az_dir))
        for yfile in sorted(yaml_files, key=str.lower):
            print "------------"
            data = _read_yaml(os.path.join(GLOSS_DIR, az_dir, yfile))
            
            print data['term']
            lst.append(data)
            dic[data['term']] = data['definition']
                
                
    with open(os.path.join(ROOT, "yoga-glossary.json"), "w") as f:
            f.write( json.dumps( lst, sort_keys=True, indent=4, separators=(',', ': ')) )
            f.close()
    with open(os.path.join(ROOT, "yoga-glossary-min.json"), "w") as f:
            f.write( json.dumps( lst  ) )
            f.close()          
            
    local("cp %syoga-glossary-min.json /home/padma/yoga-glossary-android/app/src/main/assets/yoga-glossary.json" % ROOT)
            
        