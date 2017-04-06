# -*- coding: utf-8 -*-

import os
import yaml

from fabric.api import env, local, run, lcd,  cd, sudo, warn_only, prompt
from fabric.contrib.console import confirm

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/"

GLOSS_DIR = os.path.join(ROOT, "yoga_glossary")

def _stripped(parts):
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
    
    dic = {}
    
    
    with open("Raw.txt", "r") as f:
        contents = f.read()
        
        lines = contents.split("\n")
        
        for raw_line in lines:
            line = raw_line.strip()
            if "–" in line:
                # means we got a term - description
                parts = line.split("–")
                if len(parts) > 1:
                    # split into parts
                    sparts =  _stripped(parts)	
                    
                    # the terms is first elem
                    term = sparts[0].replace("/", ", ")
                    # the a is the first letter of term
                    az = term[0].lower()
                    a2z_dir = os.path.join(GLOSS_DIR, az)
                    #print "=",  a2z_dir
                    if not os.path.exists(a2z_dir):
                        os.makedirs(a2z_dir)
                    #data = a2z[a_char]
                    
                    
                    # the defs are in elent t add
                    defs = []
                    defs_raw = " ".join(sparts[1:])
                    
                    ## rips ' of start and end
                    if defs_raw.startswith("'") and defs_raw.endswith("'"):
                        defs_raw = defs_raw[1:-1]
                    if ";" in defs_raw:
                        defs = _stripped(defs_raw.split(";"))
                    else:
                        defs = [defs_raw]
                    
                    stuff = dict(term=term, description=defs)
                    term_file_name = term.replace(" ", "_").lower() + ".yaml"
                    out_file = os.path.join(a2z_dir, term_file_name)
                    
                    ## we have to create bullshit comment
                    ## and serialise the files aout in a particular order in our case
                    # from this point forward, it is not expected
                    # that the files should ba changed in any way
                    # apart from version changes, and pull requests etc etc..
                    out_str = "term: %s\n" % term
                    out_str += "definition: \n"
                    for da in defs:
                        out_str += "  - %s\n" % da
                        
                    print out_file
                    
                    with open(out_file, "w") as ff:
                        ff.write(out_str)
                    
                else:
                    #print "  ??:", parts
                    pass
            else:
                #print "   ?:", line
                pass
    print dic.keys()		


            
        