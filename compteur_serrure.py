#!/usr/bin/env python
# -*-coding:Latin-1 -*

import hashlib
import sys
import json

from getpass import getpass
from Crypto.Cipher import AES
import base64

NOM_URL = "VIDE"
MDP_STORE = "VIDE"

ACTION_ARG = "VIDE"
MP_ANCIEN = "VIDE"
MP_NVX = "VIDE"
MP_ACT = "VIDE"
DEVICE_ARG = "VIDE"
MAC_DEVICE = "VIDE"

MDP_SERR = "VIDE"

CLE_CHIFFREMENT = "VIDE"
MSG_A_CHIFFRE = "VIDE"

NOM_SERR = "VIDE"
USER_STORE = "VIDE"

Status = 0

VERIF = False
	
def Arguments():
	
	global ACTION_ARG
	global MP_ANCIEN
	global MP_NVX
	global MP_ACT
	global DEVICE_ARG
	global Status
	global MSG_A_CHIFFRE
	global USER_ANCIEN
	
	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	if ((len(sys.argv) == 4) and (sys.argv[1] == '1')): #on recupere la liste utilisateur ou les logs ou etablit une connexion simple avec mot de passe
	
			print "Verifie ancien nouveau"
			ACTION_ARG = sys.argv[1]
			MP_ANCIEN = sys.argv[3]
			MP_ACT = sys.argv[2]
			
	if ((len(sys.argv) == 4) and (sys.argv[1] == '2')): #on recupere le mot de passe enregistre puis le compare au mdp entre
	
			print "MP actuel"
			ACTION_ARG = sys.argv[1]
			MP_ANCIEN = sys.argv[2]
			USER_ANCIEN = sys.argv[3]
			
	if ((len(sys.argv) == 3) and (sys.argv[1] == '3')): 
	
			print "Device actuel"
			ACTION_ARG = sys.argv[1]
			DEVICE_ARG = sys.argv[2]
	
	if ((len(sys.argv) == 2) and (sys.argv[1] == '4')): 
	
			print "MP_MAIL"
			ACTION_ARG = sys.argv[1]
			
	if ((len(sys.argv) == 3) and (sys.argv[1] == '5')): #chiffre mot de passe serrure
	
			print "NVX utilisateur"
			ACTION_ARG = sys.argv[1]
			MSG_A_CHIFFRE = sys.argv[2]
			
	if ((len(sys.argv) == 4) and (sys.argv[1] == '6')): #chiffre mot de passe serrure
	
			print "MP_MAIL1"
			ACTION_ARG = sys.argv[1]
			DEVICE_ARG = sys.argv[2]
			MSG_A_CHIFFRE = sys.argv[3]
								
	if ((len(sys.argv) == 3) and (sys.argv[1] == '7')): 
	
			print "dechiffre MP serrure"
			ACTION_ARG = sys.argv[1]
			DEVICE_ARG = sys.argv[2]
	
	if ((len(sys.argv) == 3) and (sys.argv[1] == '8')): 
	
			print "MP_MAIL1"
			ACTION_ARG = sys.argv[1]
			MSG_A_CHIFFRE = sys.argv[2]
			
	if ((len(sys.argv) == 2) and (sys.argv[1] == '9')): 
	
			print "MP_MAIL1"
			ACTION_ARG = sys.argv[1]
			

def MDP_Loader():

	global MDP_STORE
	global USER_STORE
	
	with open('/home/Devismes_Bridge/JSON_List/mdp.json') as f:
		dataa = json.load(f)	
		
	MDP_STORE = dataa['user']['mdp'] 
	USER_STORE = dataa['user']['user1']
	
	
def hash_new_MDP():
	
	global NVX_MDP
	mot_de_passe_chiffre = hashlib.sha256(NVX_MDP).hexdigest()
	print "nvx_mot_de_passe_chiffre", mot_de_passe_chiffre
	
	with open('/home/Devismes_Bridge/JSON_List/mdp.json') as f:
			dataa = json.load(f)	
			 
	dataa['user']['mdp'] = mot_de_passe_chiffre
		
	with open('/home/Devismes_Bridge/JSON_List/mdp.json', 'w') as f:
		json.dump(dataa, f, indent=2)	

	verrouille = True
	
def compare_mdp():
	
	global MDP_STORE #	MDP enregistre dans le JSON mdp.json
	global MP_ANCIEN # nvx MDP en vue de modification
	global VERIF 
	global USER_STORE
	global USER_ANCIEN
	global ACTION_ARG
	
	print "NVX MDP clair", MP_ANCIEN
	
	entre = MP_ANCIEN.encode()
	entre_chiffre = hashlib.sha256(entre).hexdigest()
	print "entre_chiffre", entre_chiffre
	print "MDP_STORE", MDP_STORE
	print "USER_STORE", USER_STORE
	
	if(ACTION_ARG == '2'):
	
		if ((entre_chiffre == MDP_STORE) and (USER_STORE == USER_ANCIEN)):
			VERIF = True
			print("Mot de passe ancien correct user !")
		else:
			VERIF = False
			print("Mot de passe ancien incorrec2t user !!!")
			
	else:
	
		if (entre_chiffre == MDP_STORE):
			VERIF = True
			print("Mot de passe ancien correct !")
		else:
			VERIF = False
			print("Mot de passe ancien incorrec2t !!!")
					
def change_mdp():

	global MP_ACT
	global Status
	
	LISTE_M = list(MP_ACT)
	
	print "Nouveau mot de passe !!!!" , MP_ACT
	
	if len(LISTE_M) < 8 : #le nouveau mot de passe est trop court
		Status = 3
		print "NVX mot de passe trop court !"
	else:
		with open('/home/Devismes_Bridge/JSON_List/mdp.json') as f:
			dataa = json.load(f)	
		
		entre = MP_ACT.encode()
		entre_chiffre = hashlib.sha256(entre).hexdigest()
			
		dataa['user']['mdp'] = entre_chiffre
		
		with open('/home/Devismes_Bridge/JSON_List/mdp.json', 'w') as f:
				json.dump(dataa, f, indent=2)

def charge_mac_device():

	global DEVICE_ARG
	global MAC_DEVICE
	
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as data_file:    
		jdata = json.load(data_file)
		
	MAC_DEVICE = jdata[DEVICE_ARG]["MAC"]
	
	print MAC_DEVICE
	
def Charge_MDP(): # charge MDP serrure

	global MAC_DEVICE
	global MDP
	
	MAC2 = MAC_DEVICE
	
	print "MAC2: ", MAC2

	with open('/home/Devismes_Bridge/Equipements/' + MAC2 + '/Pass.json') as f:   
			dataa = json.load(f)	

	print dataa
	P = dataa["Password"]["Pass"]
	MDP = P
	print "CHARGE_MDP_Chiffre : ", P

def charge_cle():

	global CLE_CHIFFREMENT
	
	print "Charge_cle"
	
	with open('/home/Devismes_Bridge/Equipements/clef/clef.json') as data_file:    
		jdata = json.load(data_file)
		
	CLE_CHIFFREMENT = jdata["clef"]["clef1"]
	
	print CLE_CHIFFREMENT	
	
def chiffre_mdp():

	global MSG_A_CHIFFRE
	global CLE_CHIFFREMENT
	# msg_text = 'test some plain text here'.rjust(32)
	#secret_key = '1234567890123456' # create new & store somewhere safe

	secret_key = CLE_CHIFFREMENT
	
	print secret_key
	print "MSG_A_CHIFFRE_chiffre_mdp: ", MSG_A_CHIFFRE
	msg_text = MSG_A_CHIFFRE.rjust(32)
	
	
	cipher = AES.new(secret_key,AES.MODE_ECB) 
	
	print "MSG_A_CHIFFRE_chiffre_padding: ", msg_text 
	
	encoded = base64.b64encode(cipher.encrypt(msg_text))
	print encoded
	
	MSG_A_CHIFFRE = encoded
	
	print "MSG_A_CHIFFRE" , MSG_A_CHIFFRE
	
	
def dechiffre_mdp():
	
	global MSG_A_CHIFFRE
	global CLE_CHIFFREMENT
	global MDP_SERR
	
	#C7911765AC584F50
	
	secret_key = CLE_CHIFFREMENT
	TEST8 = MSG_A_CHIFFRE #"w6hT2ggxR0tW90ZXgochRUnie1WsNSrnQ0K8dbFSejg="
	encoded = TEST8.rjust(32)
	
	print "LONGU", len(encoded)
	
	print "secret_key", secret_key
	print "MSG_A_CHIFFRE secret", encoded
	
	cipher = AES.new(secret_key,AES.MODE_ECB)

	print "secret2"
	
	msg_text = encoded
	#encoded = base64.b64encode(cipher.encrypt(msg_text))
	
	print "encoded", encoded
	
	MSG_A_CHIFFRE1 = cipher.decrypt(base64.b64decode(encoded))
	
	print "MSG_A_CHIFFRE /dechiffre", MSG_A_CHIFFRE1.strip()
	MDP_SERR = MSG_A_CHIFFRE1.strip()
	
def charge_MAC_SERR():

	global MAC_DEVICE
	global DEVICE_ARG
	
	print "recherche MAC Device"
	
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as data_file:    
		jdata = json.load(data_file)
		
	if('MAC' in jdata[DEVICE_ARG] and 'NOM' in jdata[DEVICE_ARG]):
		conv_ok = True
		MAC_DEVICE = jdata[DEVICE_ARG]["MAC"]
	else:
		conv_ok = False
	
def charge_MDP_SERR():

	global MAC_DEVICE
	global PASSWD_SERR
	global MSG_A_CHIFFRE
	global Status
	
	print "MAC Device charge, cherche MDP serrure"
	
	with open("/home/Devismes_Bridge/Equipements/"+ MAC_DEVICE + "/Pass.json") as f:
			dataa = json.load(f)	
			
	PASSWD_SERR = dataa["Password"]["Pass"]
	
	if PASSWD_SERR == "000000000000":
		Status = 7
	
	print "PASSWD_SERR: ", PASSWD_SERR 
	MSG_A_CHIFFRE = PASSWD_SERR
	
def enregistre_MDP_chiffre():

	global MSG_A_CHIFFRE
	global MAC_DEVICE
	
	print "MAC Device charge, cherche MDP serrure"
	
	with open("/home/Devismes_Bridge/Equipements/"+ MAC_DEVICE + "/Pass.json") as f:
			dataa = json.load(f)	
			
	dataa["Password"]["Pass"] =  MSG_A_CHIFFRE
	
			
	with open("/home/Devismes_Bridge/Equipements/"+ MAC_DEVICE + "/Pass.json", 'w') as f:
			json.dump(dataa, f, indent=2)
		
	
def enregistre_mail():

	global MSG_A_CHIFFRE
	
	print "enregistre_mail"
	
	with open("/home/Devismes_Bridge/JSON_List/mail.json") as f:
			dataa = json.load(f)	
			
	dataa["mail"]["MP"] =  MSG_A_CHIFFRE
			
	with open("/home/Devismes_Bridge/JSON_List/mail.json", 'w') as f:
			json.dump(dataa, f, indent=2)
			
def charge_mail():

	global MSG_A_CHIFFRE
	
	print "charge_mail"
	
	with open("/home/Devismes_Bridge/JSON_List/mail.json") as f:
			dataa = json.load(f)	
			
	MSG_A_CHIFFRE = dataa["mail"]["MP"] 
	
def change_user_name():

	global MSG_A_CHIFFRE

	with open("/home/Devismes_Bridge/JSON_List/mdp.json") as f:
			dataa = json.load(f)	
			
	dataa["user"]["user1"] =  MSG_A_CHIFFRE
			
	with open("/home/Devismes_Bridge/JSON_List/mdp.json", 'w') as f:
			json.dump(dataa, f, indent=2)

	

def Commutateur():

	global ACTION_ARG
	global MP_ANCIEN
	global MP_NVX
	global MP_ACT
	global DEVICE_ARG
	global Status
	global VERIF
	
	global MSG_A_CHIFFRE
	global CLE_CHIFFREMENT
	
	global MDP
	
	if ACTION_ARG == "1": #verifie l'ancien mot de passe puis le remplace par le nouveau
		
		print "MOT de passe CHANGE1 !!!!"
		
		MDP_Loader() #charge le mdp enregistre
		compare_mdp()
		
		if VERIF == True:
			
			print "MOT de passe CHANGE !!!!"
			Status = 1
			change_mdp()
			VERIF = False
		else:
			Status = 2
	
	if ACTION_ARG == "2": #verifie si le mot de passe de login est bon
	
		MDP_Loader()
		compare_mdp()
		
		if VERIF == True:
			VERIF = False
			Status = 1
		else:
			Status = 2
	
	if ACTION_ARG == "3": #dechiffre le mot de passe de serrure en important la cle de dechiffrement
		
		print "dechiffre le mot de passe de serrure"
		charge_mac_device()
		
		Charge_MDP() #MDP CHIFFRE
		MSG_A_CHIFFRE = MDP	
		
		charge_cle()
		
		dechiffre_mdp()
		
	if ACTION_ARG == "5":
		print "change nom utilisateur"
		change_user_name()
		
	if ACTION_ARG == "6": #sudo python motdepasse.py 6 DEVICE_3 mot_de_passe_de_serrure123456
						  #Chiffre le mot de passe de serrure et le stock dans le JSON
		print "TET6"
		charge_cle()
		charge_MAC_SERR()
		chiffre_mdp()
		enregistre_MDP_chiffre()
			
	if ACTION_ARG == "7":
	
		print "TET7"
		charge_cle() # charge la cle de chiffrement dechiffrement
		charge_MAC_SERR() # charge l'adresse mac de la serrure pour retrouver le mot de passe
		charge_MDP_SERR() # charge le mot de passe ne fonction de l'adresse MAC retrouvee
		
		if Status != 7:
			dechiffre_mdp() # dechiffre le mot de passe de la serrure et retourne le mot de passe dechiffre
			
	if ACTION_ARG == "8":
	
		print "TET8"
		charge_cle() # charge la cle de chiffrement dechiffrement
		chiffre_mdp()
		enregistre_mail()
	
	if ACTION_ARG == "9":
	
		print "TET9"
		charge_cle()
		charge_mail()
		dechiffre_mdp()
		
		
def main():
	
	global NOM_SERR
	global Status

	print("MAIN")
	print "SYS_VER:", (sys.version)
	
	Arguments()
	Commutateur()
	
	if(ACTION_ARG != '7') and (ACTION_ARG != '9'):
		print "STATUS =", Status
	else:
		if Status != 7:
			print "MDP_D:", MDP_SERR
		else: 
			print "STATUS =", Status
	
	
if __name__ == "__main__":
    main()