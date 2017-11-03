import json
import time
import subprocess
import sys

MAC_ARG = "VIDE"
ACTION_ARG = "VIDE" 
ADD_ARG	= "VIDE"
MDP_ARG	= "VIDE"
DEST_ARG = "VIDE"
MDP_SERR_ARG = "VIDE"

def mdp_serrure():

		global MAC_ARG
		global MDP_SERR_ARG
										
		with open('/home/Devismes_Bridge/Equipements/' + MAC_ARG + '/Pass.json') as f:
			dataa = json.load(f)	
		
		dataa['Password']['Pass'] = MDP_SERR_ARG
		
		with open('/home/Devismes_Bridge/Equipements/' + MAC_ARG + '/Pass.json', 'w')  as f:
			json.dump(dataa, f, indent=2)


def mail_dest():

		global DEST_ARG
										
		with open('/home/Devismes_Bridge/JSON_List/mail.json') as f:
			dataa = json.load(f)	
		
		print "OK: ", DEST_ARG
		
		dataa['mail']['Dest'] = DEST_ARG
		
		with open('/home/Devismes_Bridge/JSON_List/mail.json', 'w') as f:
			json.dump(dataa, f, indent=2)


def mail_origine():	 #base SQL !!!!
	
		global ADD_ARG
		global MDP_ARG
								
		
		with open('/home/Devismes_Bridge/JSON_List/mail.json') as f:
			dataa = json.load(f)	
		
		dataa['mail']['adresse'] = ADD_ARG	
		
		with open('/home/Devismes_Bridge/JSON_List/mail.json', 'w') as f:
			json.dump(dataa, f, indent=2)	

def Arguments():

	global MAC_ARG
	
	global ADD_ARG
	global MDP_ARG
	
	global DEST_ARG
	global MDP_SERR_ARG

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	if (len(sys.argv) == 4) and (sys.argv[1] == '1'): #on modifie le mot de passe de la serrure selectionnee
	
			print "modifie mot de passe serrure"
			MAC_ARG = sys.argv[2]
			MDP_SERR_ARG = sys.argv[3]
			mdp_serrure()
				
	if (len(sys.argv) == 3) and (sys.argv[1] == '2'): #on modifie le mail de destination 
	
			print "modifie mail destination"
			DEST_ARG = sys.argv[2]
			mail_dest()
			
	if (len(sys.argv) == 3) and (sys.argv[1] == '3'): #on modifie le mail d'origine et mot de passe
	
			print "modifie mail d'origine et mot de passe"
			ADD_ARG = sys.argv[2]	
			mail_origine()
		
def main():
	print "MAIN"
	Arguments()
	
if __name__ == "__main__":
    main()
 