#!/usr/bin/env python
# -*-coding:Latin-1 -*

import csv
import json
import re
import sys
import subprocess

NOM_SERR = "VIDE"
NOM_SERR1 = "VIDE"
MODE = "VIDE"
MAC_DEVICE = "VIDE"
conv_ok = False

def Arguments():

	global NOM_SERR
	global MODE

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	MODE = sys.argv[1]
	NOM_SERR = sys.argv[2]

def CSV_CONV_LOGS():	
	
	global MAC_DEVICE
	global NOM_SERR1
	
	with open("/home/Devismes_Bridge/Equipements/" + MAC_DEVICE +"/Logs.json") as f:
			dataa = json.load(f)	
			 
	#print dataa 
	#csv.writer(open("data.csv", "wb"), delimiter=";")

	f = csv.writer(open("/home/Devismes_Bridge/Equipements/" + MAC_DEVICE +"/Logs.csv", "wb+"), delimiter=";")
	process = subprocess.Popen("sudo chmod 644 /home/Devismes_Bridge/Equipements/" + MAC_DEVICE +"/Logs.csv", shell=True, stdout=subprocess.PIPE)
	process.wait()

	# Write CSV Header, If you dont need that, remove this line
	f.writerow(["Nom de la serrure", NOM_SERR1])
	f.writerow([""])
	f.writerow([""])
	f.writerow(["", "Action", "Heure", "Date", "Nom", "MAC"])

	i = 0

	print "LOGT" ,len(dataa)

	for i in range(1,len(dataa)):

		Num_Log = "LOG_" + str(i)
		
		print "Num_Log", Num_Log
		
		if dataa[Num_Log]["ACTION"] == "01":
			Action = "Ouvert"
		else:
			Action = "Ferme"
			

		Nom_USER = dataa[Num_Log]["NOM_USER_LOG"].decode("hex")
		MAC_USER = dataa[Num_Log]["MAC_USER_LOG"]
		
		#152108 181017 03
		DATE_HEURE_LOG_1 = dataa[Num_Log]["DATE_HEURE_LOG"]
		n = 2 
		print DATE_HEURE_LOG_1	
		
		DATE_HEURE_LOG_2 = re.findall('..?', DATE_HEURE_LOG_1)
		
		
		Heure = ''+DATE_HEURE_LOG_2[0]+':'+DATE_HEURE_LOG_2[1]+':'+DATE_HEURE_LOG_2[2]
		
		print "JOUR:", DATE_HEURE_LOG_2[6]
		JDLS = "VIDE1"
		if DATE_HEURE_LOG_2[6] == "00":
			JDLS = "Dimanche"
		if DATE_HEURE_LOG_2[6] == "01":
			JDLS = "Lundi"
		if DATE_HEURE_LOG_2[6] == "02":
			JDLS = "Mardi"
		if DATE_HEURE_LOG_2[6] == "03":
			JDLS = "Mercredi"
		if DATE_HEURE_LOG_2[6] == "04":
			JDLS = "Jeudi"
		if DATE_HEURE_LOG_2[6] == "05":
			JDLS = "Vendredi"
		if DATE_HEURE_LOG_2[6] == "06":
			JDLS = "Samedi"
			
		print "DATE_HEURE_LOG_2[3]",DATE_HEURE_LOG_2[3]
		Date = ''+ JDLS +' '+DATE_HEURE_LOG_2[3]+'/'+DATE_HEURE_LOG_2[4]+'/'+DATE_HEURE_LOG_2[5]
		
		if MAC_USER == "000000000000":
			MAC_USER2 = "NA"
		else:
			MAC_USER3 = re.findall('..?', MAC_USER)
			MAC_USER2 = MAC_USER3[0] +':'+MAC_USER3[1] +':'+MAC_USER3[2] +':'+MAC_USER3[3] +':'+MAC_USER3[4] +':'+MAC_USER3[5]
		
		f.writerow([Num_Log, Action, Heure, Date, Nom_USER, MAC_USER2])
		
def CSV_CONV_USER():	

	global NOM_SERR1
	global MAC_DEVICE 
	
	with open("/home/Devismes_Bridge/Equipements/"+ MAC_DEVICE + "/Users.json") as f:
			dataa = json.load(f)	
			 
	#print dataa 
	#csv.writer(open("data.csv", "wb"), delimiter=";")

	f = csv.writer(open("/home/Devismes_Bridge/Equipements/" + MAC_DEVICE + "/Users.csv", "wb+"), delimiter=";")
	process = subprocess.Popen("sudo chmod 644 /home/Devismes_Bridge/Equipements/" + MAC_DEVICE +"/Users.csv", shell=True, stdout=subprocess.PIPE)
	process.wait()
	# "USER_25": {
    # "NOM_USER": "4461766964", 
    # "WHITELIST": "00", 
    # "MAC_USER": "24d5175b5d68", 
    # "DROIT_USER": "01"
	# }, 

	# Write CSV Header, If you dont need that, remove this line
	f.writerow(["Nom de la serrure", NOM_SERR1])
	f.writerow([""])
	f.writerow([""])
	f.writerow(["", "Nom","MAC","Blacklist","Droits"])

	i = 0

	print "LOGT" ,len(dataa)

	for i in range(1,len(dataa)):

		Num_Log = "USER_" + str(i)
		
		print "Num_Log", Num_Log
		
			
		Nom_USER = dataa[Num_Log]["NOM_USER"].decode("hex")
		MAC_USER = dataa[Num_Log]["MAC_USER"]
		WHITELIST = dataa[Num_Log]["WHITELIST"]
		DROIT_USER = dataa[Num_Log]["DROIT_USER"]
		
		if MAC_USER == "000000000000":
			MAC_USER2 = "NA"
		else:
			MAC_USER3 = re.findall('..?', MAC_USER)
			MAC_USER2 = MAC_USER3[0] +':'+MAC_USER3[1] +':'+MAC_USER3[2] +':'+MAC_USER3[3] +':'+MAC_USER3[4] +':'+MAC_USER3[5]
			
		if WHITELIST == "00":
			WHITELIST2 = "NON"
		if WHITELIST == "01":
			WHITELIST2 = "OUI"	
		
		if DROIT_USER == "00":
			DROIT_USER1 = "Utilisateur"
		if DROIT_USER == "01":
			DROIT_USER1 = "Administrateur"	
		
		f.writerow([Num_Log, Nom_USER, MAC_USER2, WHITELIST2, DROIT_USER1])
		
def recherche_user():

	global MAC_DEVICE
	global NOM_SERR
	global conv_ok
	global NOM_SERR1
	
	print "recherche"
	
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as data_file:    
		jdata = json.load(data_file)
		
	if('MAC' in jdata[NOM_SERR] and 'NOM' in jdata[NOM_SERR]):
		conv_ok = True
		MAC_DEVICE = jdata[NOM_SERR]["MAC"]
		NOM_SERR1 = jdata[NOM_SERR]["NOM"]
	else:
		conv_ok = False
		
def main():
	
	global NOM_SERR
	global MODE
	global conv_ok
	
	print("MAIN")
	print "SYS_VER:", (sys.version)
	Arguments()
	recherche_user()
	
	if (conv_ok == True):
	
		if MODE == '1':
			CSV_CONV_LOGS()
		if MODE == '2':
			CSV_CONV_USER()

	


		
if __name__ == "__main__":
    main()
 
 
	
