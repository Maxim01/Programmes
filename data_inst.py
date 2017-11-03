#!/usr/bin/env python
# -*-coding:Latin-1 -*

import re
import sys
import subprocess

NOM_URL = "VIDE"
URL = "VIDE"
CODE = "VIDE"

def Arguments():

	global NOM_URL

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	for i in range (0,len(sys.argv)):
		print sys.argv[i]
		
	NOM_URL = sys.argv[1] 
		
def parser():
		
	global NOM_URL
	global CODE
	
	liste = NOM_URL.split()
	print liste
	URL = liste[1]
	print URL
	URL2 = re.split(r"/", URL)
	print URL2[3]
	URL3 = re.split(',|\.', URL2[3])
	CODE = URL3[0]
	
def installeur():

	global CODE
	
	URL3 = "curl https://www.dataplicity.com/" + CODE +'.py | sudo python'
	#print "CODE", URL3
	
	process = subprocess.Popen([URL3], stdout=subprocess.PIPE, shell=True)
	process.wait()
	(out, err) = process.communicate()
	Data_Scan = out
	print Data_Scan

	
		
def main():
	
	global NOM_SERR

	print("MAIN")
	print "SYS_VER:", (sys.version)
	Arguments()
	parser()
	installeur()
	

if __name__ == "__main__":
    main()
 
 
	
