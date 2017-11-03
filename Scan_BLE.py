import subprocess
import re
import time
import json
import sys
import os
import datetime
import binascii
from time import gmtime, strftime 
	
#while(1):
#time.sleep(2)

Numero_device = 0		
compteur_device = 0
Data_Scan = "VIDE"
Nb_elmts_device = "VIDE"
liste1 = "VIDE"

DEVI  = False
COMPL = False
MANUFA = False
MANUFA_DEV = False
WL_Device1 = False

MAC_fusion = "VIDE"
RSSI_fusion = "VIDE"
MANUF_fusion = "VIDE"
NOM_fusion = "VIDE"
ETAT_penes = "VIDE"
ETAT_surv = "VIDE"
BATT_fusion = "VIDE"

NUM_DEV = '0'

def Arguments():

	global DEVICE_ARG
	global USER_MODIF_ARG
	global ACTION_ARG
	global DROITS_ARG

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	#if ((len(sys.argv) == 2) and (sys.argv[2] == '1')): #on veut reset la liste des equipements
	
	
def Start_Scan():

	global Data_Scan


	print "Start_scan !"

	proc = subprocess.Popen(["sudo blescan -t 2"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	#print "program output:", out

	Data_Scan = out.splitlines()
	#print "program data:", len(data)

	if len(Data_Scan)<6 :
		longeur = False
	else:
		longeur = True

	for i in range(1,len(Data_Scan)):
	  print Data_Scan[i]
	  
	print("longu")
	print("{}").format(len(Data_Scan))
	
 
def Parse_Device():

	global Data_Scan
	global compteur_device
	global Nb_elmts_device
	global liste1

	for i in range(1,len(Data_Scan)): # tous les devices
		s = str(Data_Scan[i])
		data2 = s.split()
		
		if data2[0] == "Device":	
		 compteur_device = compteur_device + 1
		 
	print "NB_Device:", compteur_device
	fin_device = 1

	liste1 = ['y' for e in range(compteur_device)]
	Nb_elmts_device = ['y' for e in range(compteur_device)] # pour creer une table vide
	print "liste1", liste1

	compteur_liste = 0

	for i in range(1,len(Data_Scan)): # tous les devices
		s = str(Data_Scan[i])
		data2 = s.split()
		
		if data2[0] == "Device":	
			 liste1[compteur_liste] = i
			 compteur_liste = compteur_liste + 1
		 
	print "Lignes: ", liste1

	NB_elmts_total = 0 #moins le dernier device
		 
	if compteur_device > 1: #il existe plusieurs equipements
		for i in range(0,compteur_device-1):
			Nb_elmts_device[i] = liste1[i+1] - liste1[i]
			NB_elmts_total = NB_elmts_total + Nb_elmts_device[i]
		Nb_elmts_device[compteur_device-1] = len(Data_Scan)- (NB_elmts_total+1)
		
	if compteur_device == 1:
		Nb_elmts_device[0] = len(Data_Scan)-1

	print "NB_elts_Device", Nb_elmts_device

	ansi_escape = re.compile(r'\x1b[^m]*m')

#print 'Nombre equipenents:', data7['Nombre_Device']


def Init_File():
	open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w').close()	
	data8 = {}  

	with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as outfile:  
		json.dump(data8, outfile)

		
def Heure_Scan_Device():
	
	global RSSI_fusion
	global BATT_fusion
	global ETAT_surv
	global ETAT_penes
	global NUM_DEV
	
	if DEVI == True and COMPL == True and MANUFA == True and MANUFA_DEV == True:
								
		Device_name	= "Device_" + str(NUM_DEV);
		print "Enregistement OK"
		
		
		Heure_Scan = strftime("%H:%M:%S   %d/%m/%Y", time.localtime())
		# Heure_Scan = datetime.datetime.now()
		DATE_MAX = str(Heure_Scan)
		
		with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
			dataa = json.load(f)	
			 
		dataa[Device_name]['RSSI'] = RSSI_fusion
		dataa[Device_name]['Heure_Scan'] = DATE_MAX
		dataa[Device_name]['BATT'] = BATT_fusion
		dataa[Device_name]['VISIBLE'] = 'OUI'
		dataa[Device_name]["ETAT_surv"] = ETAT_surv
		dataa[Device_name]['ETAT_penes'] = ETAT_penes
			
		with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as f:
			json.dump(dataa, f, indent=2)	

def Invisible1():

	global MAC_fusion
	global Numero_device
	global NUM_DEV
	global NUM_DEV2
	
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as data_file:    
		jdata = json.load(data_file)
			
			
	print "INVISBLE1!!!!!"
	#nombre de device dans le json
	
	NUM = 1
	Test_Device =  "Device_" + str(NUM) in jdata
		
	while Test_Device == True:
		print "OK_True", NUM
		NUM = NUM + 1
		Test_Device =  "Device_" + str(NUM) in jdata

	Test_MAC = False
		
	for i in range(0,NUM-1):
		NUM_DEV2 = str(i+1)
		Invisible()	
					
def Invisible():
		
	global NUM_DEV2
									
	Device_name	= "Device_" + str(NUM_DEV2);
	print "Invisible OK", str(NUM_DEV2)
			
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
		dataa = json.load(f)	
		 
	dataa[Device_name]['VISIBLE'] = 'NON'
		
	with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as f:
		json.dump(dataa, f, indent=2)	
	

def Nouveau_Device():  #associe le numero de device a l adresse MAC

	global MAC_fusion
	global Numero_device
	global NUM_DEV
	global NUM_DEV2
	
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as data_file:    
		jdata = json.load(data_file)
			
	#nombre de device dans le json
	
	NUM = 1
	Test_Device =  "Device_" + str(NUM) in jdata
		
	while Test_Device == True:
		print "OK_True", NUM
		NUM = NUM + 1
		Test_Device =  "Device_" + str(NUM) in jdata

	Test_MAC = False
		
	for i in range(0,NUM-1):
	
		Test_Device = "Device_" + str(i+1) in jdata
		
		if Test_Device == True:
			MAC_DEVICE = jdata["Device_" + str(i+1)]["MAC"]
			print "MAC_DEVICE", MAC_DEVICE
			print "MAC_fusion", MAC_fusion
			
			if MAC_fusion == MAC_DEVICE:
				print "Device_existant:",  i+1
				NUM_DEV = str(i+1)
				NUM_DEV2 = str(i+1)
				Test_MAC = True
								
	if 	(Test_MAC == False or NUM == 1) and MAC_fusion != 'VIDE': # Le device n'existe pas
		Numero_device = NUM;
		Ajoute_Nouveau_Device()
		#Heure_Scan_Device()
		Creation_Dossier()
	else:	
		#Invisible2()
		if (MAC_fusion != 'VIDE'):
			Creation_Dossier()
			Heure_Scan_Device() # actualise scan + Rssi + visiblite
			WL_Device()
	
			
	#for i in range(0,compteur_device): 
	
	#print "json_size", jdata
	
def Creation_Dossier():

	global MAC_fusion
	
	file_path = "/home/Devismes_Bridge/Equipements/" + MAC_fusion + "/test.txt"
	
	print "file_path", file_path
	directory = os.path.dirname(file_path)
	print "directory", directory	
	
	if not os.path.exists(directory):
		os.makedirs(directory)
		print "EXIST 2"
		file1 = open('/home/Devismes_Bridge/Equipements/' + MAC_fusion + '/Logs.json', 'w+')
		file1.write("{}")
		file2 = open('/home/Devismes_Bridge/Equipements/' + MAC_fusion + '/Users.json','w+')
		file2.write("{}")
		file3 = open('/home/Devismes_Bridge/Equipements/' + MAC_fusion + '/Pass.json', 'w+')
		file3.write('{"Password":{"Pass":"000000000000"}}')
	else:
		print "EXIST 3"
	

def Ajoute_Nouveau_Device():
    
	global MAC_fusion
	global RSSI_fusion
	global MANUF_fusion
	global NOM_fusion
	global ETAT_penes
	global ETAT_surv
	global BATT_fusion
	global Numero_device
	
	if DEVI == True and COMPL == True and MANUFA == True and MANUFA_DEV == True:
								
		Device_name	= "Device_" + str(Numero_device);
		print "Enregistement OK nouveau"
		
		Heure_Scan = strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		DATE_MAX = str(Heure_Scan)
		VISIBLE = 'OUI'		
		a_dict1 = {Device_name: 	{'MAC': MAC_fusion, 
									'RSSI': RSSI_fusion, 
									'MANUF': MANUF_fusion, 
									'NOM': NOM_fusion, 
									'ETAT_penes': ETAT_penes, 
									'ETAT_surv': ETAT_surv, 
									'BATT': BATT_fusion, 
									'Heure_Scan': DATE_MAX, 
									'VISIBLE': VISIBLE, 
									'WL': '0',
									'USER_CONN':'0',
									'LOG_CONN':'0'}}

		with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
			dataa = json.load(f)	
			 
		dataa.update(a_dict1)
			
		with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as f:
			json.dump(dataa, f, indent=2)	
			
		
def WL_Device():

	global NUM_DEV2
	global WL_Device1
										
	Device_name	= "Device_" + str(NUM_DEV2);
	
			
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
		dataa = json.load(f)	

	if dataa[Device_name]['WL'] == '0': #le device n'est deja whiteliste
		WL_Device1 = False
		print "N'est pas deja WL_DEVICE MAX TRUE"
		
	if dataa[Device_name]['WL'] == '1': #le device est deja whiteliste
		WL_Device1 = True
		print "Deja WL_DEVICE"
		

			
def Reaction_Device():

	global Alarme
	global Modif_U
	global Modif_L
	global Numero_device
	global WL_Device1
	global NOM_fusion
	global NUM_DEV
	
	global NUM_DEV2
	
	#WL_Device on whitelist le device si le mot de passe rece en trame 41
	
	if Alarme == "1" and WL_Device1 == True: #l'alame est enclenchee //envoyer mail a qqun
		print "ALARME ALARME ALARME ALARME ALARME ALARME "
		process = subprocess.Popen(["sudo python /home/Devismes_Bridge/Programmes/laposte.py " + NOM_fusion + ' ' + '1'], stdout=subprocess.PIPE, shell=True)
		process.wait()
		(out, err) = process.communicate()
		  #verifier si mot de passe ajoute
	if Modif_U == "1" and WL_Device1 == True: #une modif sur la liste user a eu lieu
		print "Modif_U Modif_U Modif_U Modif_U Modif_U  "
		print "Numero_device", NUM_DEV
		
		Device_name	= "Device_" + str(NUM_DEV2);
		
		with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
			dataa = json.load(f)	
		 
		if dataa[Device_name]["USER_CONN"] == "0":
			print "Reactualisation user"
			process = subprocess.Popen("sudo python /home/Devismes_Bridge/Programmes/Loader_BLE.py Device_" + str(NUM_DEV) + " " + "1", shell=True, stdout=subprocess.PIPE)
			process.wait()
			(out, err) = process.communicate()
			Data_Scan = out.splitlines()
			#print Data_Scan
		
	if Modif_L == "1" and WL_Device1 == True: #une modif sur les logs a eu lieu
		print "Modif_L Modif_L Modif_L Modif_L Modif_L " 
		print "Numero_device LOGS", Numero_device
		
		Device_name	= "Device_" + str(NUM_DEV2);
		
		with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
			dataa = json.load(f)	
		
		if dataa[Device_name]["LOG_CONN"] == "0":
			print "Reactualisation logs"
			process = subprocess.Popen("sudo python /home/Devismes_Bridge/Programmes/Loader_BLE.py Device_" + str(NUM_DEV) + " " + "2", shell=True, stdout=subprocess.PIPE)
			process.wait()
			(out, err) = process.communicate()
			Data_Scan = out.splitlines()
			print Data_Scan
		
		#os.system("sudo python Loader_BLE.py Device_" + str(Numero_device) + " " + "2")
		
def Test_Equipement():

	global Data_Scan
	global Numero_device
	
	global DEVI  
	global COMPL 
	global MANUFA
	global MANUFA_DEV
	
	global MAC_fusion
	global RSSI_fusion
	global MANUF_fusion
	global NOM_fusion
	global ETAT_penes
	global ETAT_surv
	global BATT_fusion
	
	global NUM_DEV
	
	global Alarme
	global Modif_U
	global Modif_L
	
	data = Data_Scan
	
	for i in range(0,compteur_device): # a completer
		
		print "NB_elt_device", Nb_elmts_device[i]
		
		if Nb_elmts_device[i] == 5:   #il y a 5 elements dans le device y compris le device lui meme
		
			s1 = str(data[liste1[i]])
			data2 = s1.split()
			s2 = str(data[liste1[i]+3])
			data3 = s2.split()
			s3 = str(data[liste1[i]+4])
			data4 = s3.split()

			print i
			print "data2: ", data2
			print "data3: ", data3
			print "data4: ", data4
			
			DEVI  = False
			COMPL = False
			MANUFA = False
			MANUFA_DEV = False
			
			if data2[0] == "Device" and data2[1] == "(new):" :
				
				DEVI  = True
				Numero_device = Numero_device + 1
				print "Numero_device: ", Numero_device
				print("{}").format(data2[0])
				#print("{}").format(data2[2])
				
				tab_adv_mac = list(str(data2[2]))
				tab_adv_mac_char =  ["\0"] * (len(tab_adv_mac)-9)
						
				for j in range(5,len(tab_adv_mac)-4):
					tab_adv_mac_char[j-5] = tab_adv_mac[j]
					#print("{}").format(tab_adv_nom[j])
					
				MAC_fusion = ''.join(tab_adv_mac_char)
				print("{}").format(MAC_fusion)	
				
				print "RSSI: "
				print("{}").format(data2[4])
				RSSI_fusion = ''.join(data2[4])
			
			if data3[0] == "Complete" and data3[1] == "Local" and data3[2] == "Name:":
			
				COMPL = True
				print "Nom: "
				tab_adv_nom = list(str(data3[3]))
				NOM_fusion_i = ''.join(tab_adv_nom)
				NON_ANSI =  re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', NOM_fusion_i)
				print "NOM_fusion_i", NON_ANSI	
				NOM_fusion = NON_ANSI.replace("'", "")		
				print("{}").format(NOM_fusion)
				print "NOM_fusion_fin: " , NOM_fusion
				
			if data4[0] == "Manufacturer:":
				
				MANUFA = True
				MANUF_fusion = ''.join(data4[1])
				MANUF_fusion = MANUF_fusion.replace(">", "")
				MANUF_fusion = MANUF_fusion.replace("<", "")
				print "manuf: ", MANUF_fusion
				
			data_man =  list(MANUF_fusion)
			print "NOM_fusion_split: " , data_man
			
			#['4', '4', '6', '5', '7', '6'}
			
			if data_man[0] == "4" and data_man[1] == "4" and data_man[2] == "6" and data_man[3] == "5" and data_man[4] == "7" and data_man[5] == "6":
				MANUFA_DEV = True
				print "DEV OK"
				
			if MANUFA_DEV == True:
				#446576ffbeb22b4a5203c9 -> 446576 ffbeb22b4a52 03 c9
				liste_man_etat = [data_man[18], data_man[19]]
				liste_man_pourcent = [data_man[20], data_man[21]]
				Etat_Serrure = ''.join(liste_man_etat)
				Pourcent_batt = ''.join(liste_man_pourcent)
				
				print "etat: ", Etat_Serrure
				print "pourcent batt: ", Pourcent_batt
			
				BINAR = bin(int(Etat_Serrure, 16))[2:].zfill(8)
				Bin_LIST = list(BINAR)
				
				
				print 'ES', Etat_Serrure
				print "BINAR", str(BINAR)
				print "Bin_LIST", str(Bin_LIST)
				
				if Bin_LIST[7] == '0':  #surverrouillage
					ETAT_surv = "0"
				else:
					ETAT_surv = "1"
				
				if Bin_LIST[6] == '0':  #penes
					ETAT_penes = "0"
				else:
					ETAT_penes = "1"				
					
				if Bin_LIST[5] == '0':  #Ouverture auto
					Ouverture_Auto = "0"
				else:
					Ouverture_Auto = "1"	
					
				if Bin_LIST[4] == '0':  #Alarme
					Alarme = "0"
				else:
					Alarme = "1"
					
				if Bin_LIST[3] == '0':  #Modif_Liste_user
					Modif_U = "0"
				else:
					Modif_U = "1"
					
				if Bin_LIST[2] == '0':  #Modif_Liste_logs
					Modif_L = "0"
				else:
					Modif_L = "1"
										
				Pourcent_batt_int = int(Pourcent_batt, 16)
				print "pourcent batt2: ", Pourcent_batt_int
				
				if Pourcent_batt_int > 100:
					BATT_fusion = (Pourcent_batt_int - 128)
				else:
					BATT_fusion = Pourcent_batt_int
					
				print "BATT_fusion: ", BATT_fusion
				Nouveau_Device()
				print "NUM_DEV_MAX", NUM_DEV
				Reaction_Device()
				
				
# def Creation_Dossier_Device():
	
	# file_path = "/home/Devismes_Bridge/JSON_List/mail.json"
		
	# if not os.path.exists(file_path):
		# print "EXIST Device = Create"
		# file1 = open('/home/Devismes_Bridge/JSON_List/mail.json', 'w+')
		# file1.write('{"mail": {"Dest": "VIDE", "adresse": "VIDE", "MP": "VIDE"}}')
	# else:
		# print "EXIST Device = OK"
				
def Creation_Dossier_Device():
	
	file_path1 = "/home/Devismes_Bridge/JSON_List/mdp.json"
	file_path2 = "/home/Devismes_Bridge/JSON_List/mail.json"
	file_path3 = "/home/Devismes_Bridge/JSON_List/Last_connected.json"
	file_path4 = "/home/Devismes_Bridge/JSON_List/Devices.json"
	file_path5 = "/home/Devismes_Bridge/Equipements/clef/clef.json"
	
	directory = os.path.dirname(file_path1)
	
	if not os.path.exists(directory):
		os.makedirs(directory)
		
	if not os.path.exists(file_path1):
		print "EXIST Device = Create mdp"
		file1 = open('/home/Devismes_Bridge/JSON_List/mdp.json', 'w+')
		file1.write('"user": {"mdp": "32dd86af46c29ccd6c1a9ab7b02ba4fbf417e72af3adfa93e3394fb1d81ed847", "change": "0", "user1": "Devismes"}')
	
	if not os.path.exists(file_path2):
		print "EXIST Device = Create mail"
		file2 = open('/home/Devismes_Bridge/JSON_List/mail.json', 'w+')
		file2.write('{"mail": {"Dest": "VIDE", "adresse": "VIDE", "token": "VIDE", "MP": "VIDE", "sid": "VIDE", "num_envoi": "VIDE", "num_recep": "VIDE"}}')	
	
	if not os.path.exists(file_path3):
		print "EXIST Device = Create last"
		file3 = open('/home/Devismes_Bridge/JSON_List/Last_connected.json', 'w+')
		file3.write('{"Heure_ref": {"DATE_MAX": "VIDE"}, "Heure": {"Conn": 0, "DATE_MAX": "VIDE"}}')	
	
	if not os.path.exists(file_path4):
		print "EXIST Device = Create device"
		file4 = open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w+')
		file4.write('{}')	
		
	directory = os.path.dirname(file_path5)
	
	if not os.path.exists(directory):
		os.makedirs(directory)
		
	if not os.path.exists(file_path5):
		print "EXIST Device = Create clef"
		file5 = open('/home/Devismes_Bridge/Equipements/clef/clef.json', 'w+')
		RAND_M = binascii.b2a_hex(os.urandom(8))
		file5.write('{"clef": {"clef1":"'+ RAND_M +'"}}')	
	
		
			
def MAC_PI_GET():

	open('/home/Devismes_Bridge/JSON_List/MAC_PI.json', 'w').close()	 #RAZ fichier
	data8 = {}  

	with open('/home/Devismes_Bridge/JSON_List/MAC_PI.json', 'w') as outfile:  
		json.dump(data8, outfile)
		
	proc = subprocess.Popen(["hciconfig -a"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	#print "program output:", out

	data = out.splitlines()
	s = str(data[1])
	data2 = s.split()
	print "MAC:", data2[2]
	MAC = data2[2]

	a_dict1 = {'MAC': data2[2]}

	with open('/home/Devismes_Bridge/JSON_List/MAC_PI.json') as f:
		datab = json.load(f)	
					 
	datab.update(a_dict1)
					
	with open('/home/Devismes_Bridge/JSON_List/MAC_PI.json', 'w') as f:
		json.dump(datab, f)
					
				
def main():
	
	print("MAIN")
	print "SYS_VER:", (sys.version)
	
	Creation_Dossier_Device()
	
	Invisible1()
	Start_Scan()
	Parse_Device()
	Test_Equipement()
		
if __name__ == "__main__":
    main()
 
			
		
	
