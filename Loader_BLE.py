#!/usr/bin/env python
# -*-coding:Latin-1 -*

# MODIF_LISTE python -OO -m py_compile Modif_liste_Pi.py compiler obscussisement

import pexpect
import time
import json
import subprocess
import sys
import struct
import re
import crc16 
import crcmod
import binascii
import os
import encodings
import datetime

from time import sleep
from time import gmtime, strftime 

import io
import shutil

from logging import basicConfig, getLogger

from Crypto.Cipher import AES

from rubenesque.codecs.sec import encode, decode
import rubenesque.curves
secp256r1 = rubenesque.curves.sec.secp256r1

sys.setrecursionlimit(10000000)

#BOOLEENS
Device_Connect = False

#TRAMES

NOM_RPI = 'Raspberry'
MDP = 'C7911765AC584F50'

MAC_DEVICE = '000000000000' 
MAC_RPI = '000000000000' 

TRAME_VIDE_31 = '00000000000000000000000000000000'
TRAME_VIDE_32 = '00000000000000000000000000000000'
TRAME_VIDE_34 = '00000000000000000000000000000000'
TRAME_VIDE_64 = list(TRAME_VIDE_32)

TRAME_Recue = ['00','00','00','00','00','00','00']

#CLES + NONCE
# global CLE_P11 
# global CLE_P12 
# global CLE_P21 
# global CLE_P22 
# global NONCE 
# global SHARED

CLE_P11 = '00000000000000000000000000000000'
CLE_P12 = '00000000000000000000000000000000'
CLE_P21 = '00000000000000000000000000000000'
CLE_P22 = '00000000000000000000000000000000'
NONCE = '00000000000000000000000000000000'
SHARED = '00000000000000000000000000000000'

RECU_65 = '00000000000000000000000000000000'
RECU_66 = '00000000000000000000000000000000'
RECU_67 = '00000000000000000000000000000000'
RECU_68 = '00000000000000000000000000000000'
RECU_69 = '00000000000000000000000000000000'

RECU_32 = False
RECU_41 = False
RECU_50 = False
RECU_60 = False

PLUS_DE_LOGS = False

hex_int_8 = 0

NB_USER = 0
NOM_USER = 'DEFAUT'
MAC_USER = '000000000000'
DROIT_USER = '00'
WHITELIST = '04'

NOM_USER_LOG = 'DEFAUT'
MAC_USER_LOG = '000000000000'
ACTION = '0'
DATE_HEURE_LOG = '00000000'

MAC_UTILISATEUR_MODIF = 'fbf27d4bd378' #'000000000000'
DROITS_MODIF = '00'

MAC_UTILISATEUR_SUPPR = '9b9d2399257b'

DEVICE_ARG = 'DEVICE_0'
USER_MODIF_ARG = 'USER_0'
ACTION_ARG = '0' #zero
DROITS_ARG = 'N' #neutre

MODE_CONNEXION_1 = '1' #0 recupere liste utilisateur

test1 = False
test2 = False 
test3 = False
test4 = False
test5 = False

STATUS_ERR = False
STATUS_ERR2 = False
STATUS_ERR3 = '00'

def Arguments():

	global DEVICE_ARG
	global USER_MODIF_ARG
	global ACTION_ARG
	global DROITS_ARG

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	if (len(sys.argv) == 3) and ((sys.argv[2] == '1') or (sys.argv[2] == '2') or (sys.argv[2] == '5')): #on recupere la liste utilisateur ou les logs ou etablit une connexion simple avec mot de passe
	
			print "Demande user ou logs"
			DEVICE_ARG = sys.argv[1]
			ACTION_ARG = sys.argv[2]
			
	if (len(sys.argv) == 4) and (sys.argv[2] == '4'): #supprime droits utlisateur en fct de son adresse MAC
	
			print "Supprime utlisateur"
			DEVICE_ARG = sys.argv[1]
			ACTION_ARG = sys.argv[2]
			USER_MODIF_ARG = sys.argv[3] #ex: USER_4
	
	if (len(sys.argv) == 5) and (sys.argv[2] == '3'): #modifie utilisateur en fct de son adresse mac
	
			print "Modifie utlisateur"
			DEVICE_ARG = sys.argv[1]
			ACTION_ARG = sys.argv[2]
			USER_MODIF_ARG = sys.argv[3]
			DROITS_ARG = sys.argv[4]
			
	
		
def Charger_Device():

	global MAC_DEVICE
	global MAC_RPI
	global DEVICE_ARG
	
	global Test_Presence_Device
	
	#{"Device_1": {"MANUF": "<5555446576d1f7b198bd3900>", "RSSI": "-59", "MAC": "d1:f7:b1:98:bd:39", "NOM": "SerrureDavid"}}
	#DEVICE = "ce:45:bc:d4:32:0b"
	# sudo gatttool -b e9:e5:e3:72:12:5a -t random --interactive

	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as data_file:    
		jdata = json.load(data_file)
		
		
	# with open('Save_JSON/SAVE_MP_SERRURE.json') as data_file3:    
		# MOT_J = json.load(data_file3)

	TEST41 = DEVICE_ARG
	
	print "TEST41", TEST41
		
	# MDP = MOT_J['MP']
	#MDP = 'AZERTYUIOP'

	test1 =  TEST41 in jdata
	test2 = False
	test3 = False
	test4 = False
	test5 = False

	if test1 == True:
		#print ("Vrai1")
		test2 =  'MANUF' in jdata[TEST41]
		test3 =  'RSSI' in jdata[TEST41]
		test4 =  'MAC' in jdata[TEST41]
		test5 =  'NOM' in jdata[TEST41]
	else:
		#EMPTY = 4
		print ("DEVICE non existant")

	if test2 == True:
		print ("Vrai2")
	else:
		print ("Faux2")

	if test3 == True:
		print ("Vrai3")
	else:
		print ("Faux3")

	if test4 == True:
		print ("Vrai4")
	else:
		print ("Faux4")
		
	if test5 == True:
		print ("Vrai5")
	else:
		print ("Faux5")
		
	if((test1 == True) and (test2 == True) and (test3 == True) and (test4 == True) and (test5 == True)):
		Test_Presence_Device = True
		MAC_DEVICE = jdata[TEST41]["MAC"]
		Charge_MDP()
	else:
		Test_Presence_Device = False
	

def Charge_MDP():

	global MAC_DEVICE
	global MDP
	
	MAC2 = MAC_DEVICE
	
	print "MAC2: ", MAC2
		
		
	# e9:e5:e3:72:12:5a
	with open('/home/Devismes_Bridge/Equipements/' + MAC2 + '/Pass.json') as f:   
			dataa = json.load(f)	
			
	# with open('/home/Devismes_Bridge/Equipements/e9:e5:e3:72:12:5a/Pass.json') as f:   
			# dataa = json.load(f)
	
	print dataa
	P = dataa["Password"]["Pass"]
	MDP = P
	print "CHARGE_MDP : ", P
	
		
def Connexion_Device():	

	global MAC_DEVICE
	global NONCE
	global Device_Connect
	
	#MAC_DEVICE =
	#print("Addresse Serrure:"),
	#print(MAC_DEVICE)
	 
	# Run gatttool interactively.
	#print("Lancement gatttool...")

	# proc1 = subprocess.Popen(["sudo hciconfig hci0 down"], stdout=subprocess.PIPE, shell=True)  #fermet et reouvre les interfaces pour les demarrer proprement
	# time.sleep(0.5)
	# proc2 = subprocess.Popen(["sudo hciconfig hci0 up"], stdout=subprocess.PIPE, shell=True)
	# time.sleep(0.5)

	global child
	
	child = pexpect.spawn("sudo gatttool -b " + MAC_DEVICE + " -t random --interactive")
	
	# Connect to the device.

	non_connecte = 1
	non_chiffre = 1
	nb_tentative = 0
	connexion_OK = False

	while non_connecte :

		#print("Connecting to "),
		#print(MAC_DEVICE),
		child.sendline("connect")

		# child.timeout = 5

		i = child.expect(['Connection successful', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 

		##print child.before, child.after
		
		nb_tentative = nb_tentative + 1
		
		#print("Tentative "), nb_tentative
		
		if nb_tentative  == 5:
			print("Nombre de tentative = 5, fin de la tentatative de connexion")
			non_connecte = 0
			connexion_OK = False
				
		if i == 0: # ok
			# #print 'OK'
			print("Connexion reussie !")
			connexion_OK = True
			non_connecte = 0
		if i == 1: 
			#print 'ERROR!'
			#print child.after
			connexion_OK = False
				
		if i == 2: # EOF
			#print 'EOF'
			connexion_OK = False
				
		if i == 3: # timeout
			print 'timeout'
			connexion_OK = False

	if connexion_OK == True:
		#print ("TEST OK")
		Device_Connect = True
	
def Attente_trame_69(OPCODE):
	
	global STATUS_ERR
	global RECU_65
	global RECU_66
	global RECU_67
	global RECU_68
	global RECU_69
	
	connexion_OK = False

	j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 

	if j == 0: # ok
		# #print 'OK'
		#print "Reception reussie !" , OPCODE
		connexion_OK = True
		non_connecte = 0
	if j == 1: 
		#print 'ERROR!'
		#print child.after
		connexion_OK = False
			
	if j == 2: # EOF
		#print 'EOF'
		connexion_OK = False
			
	if j == 3: # timeout
		#print 'timeout'
		connexion_OK = False
	if connexion_OK == True:

		# print("Recption reussie 2 !")
		STATUS_ERR = False

		if OPCODE == '65':
			# print "65 recu"
			RECU_65 = child.after
		if OPCODE == '66':
			# print "66 recu"
			RECU_66 = child.after
		if OPCODE == '67':
			# print "67 recu"
			RECU_67 = child.after
		if OPCODE == '68':
			# print "68 recu"
			RECU_68 = child.after
		if OPCODE == '69':
			# print "69 recu"
			RECU_69 = child.after		
	else:
		STATUS_ERR = True
		print "ERREUR RECEPTION: ", OPCODE
	
def Chiffrement_ECDH():

		child.sendline("char-write-req 0x000e 0100 --listen")

		global alice_prv 
		global CLE_P11
		global CLE_P12
		global CLE_P21
		global CLE_P22
		global NONCE
		global STATUS_ERR

		global RECU_65
		global RECU_66
		global RECU_67
		global RECU_68
		global RECU_69
		
		alice_prv = secp256r1.private_key()
		
		 
		#EX: alice_prv = 84339034994899829689617173601102277207976898122161641093429757367264161246220
		alice_pub = secp256r1.generator() * alice_prv
		##print alice_pub

		ALIC_PRV = str(alice_prv)
		ALIC_PUB = str(alice_pub)

		s7 = str(ALIC_PUB)
		s7 = s7.replace(",", "")
		s7 = s7.replace("(", " ")
		s7 = s7.replace(")", " ")		
		data7 = s7.split()

		ALIC_PUB1 = data7[1]
		ALIC_PUB2 = data7[2]

		##print "DATA", data7
		##print "A_PRV", ALIC_PRV

		ALIC_PUB17= int(ALIC_PUB1 , 16)

		##print "A_pub1",ALIC_PUB17

		ALIC_PUB27 = int(ALIC_PUB2 , 16)

		##print "A_pub2",ALIC_PUB27

		ALIC_PUB11 = ALIC_PUB1[0:32]
		ALIC_PUB12 = ALIC_PUB1[32:64]
		ALIC_PUB21 = ALIC_PUB2[0:32]
		ALIC_PUB22 = ALIC_PUB2[32:64]

		PUB1 = "65" + ALIC_PUB11 + "0000"			# en fonction de la cle privee

		##print "PUB1", PUB1

		child.sendline("char-write-cmd 0x0010 " + PUB1)
		time.sleep(0.1)

		PUB2 = "66" + ALIC_PUB12 + "0000"		
		child.sendline("char-write-cmd 0x0010 " + PUB2)
		time.sleep(0.1)

		PUB3 = "67" + ALIC_PUB21 + "0000"			
		child.sendline("char-write-cmd 0x0010 " + PUB3)
		time.sleep(0.1)

		PUB4 = "68" + ALIC_PUB22 + "0000"		
		child.sendline("char-write-cmd 0x0010 " + PUB4)


		# j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 
		# RECU_65 = child.after
			
		# j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 
		# RECU_66 = child.after

		# j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 
		# RECU_67 = child.after

		# j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 
		# RECU_68 = child.after

		# j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 
		# RECU_69 = child.after
		
		if STATUS_ERR == False:
			# print "65 att"
			Attente_trame_69('65')

			if STATUS_ERR == False:
				# print "66 att"
				Attente_trame_69('66')

				if STATUS_ERR == False:
					# print "67 att"
					Attente_trame_69('67')

					if STATUS_ERR == False:
						# print "68 att"
						Attente_trame_69('68')

						if STATUS_ERR == False:
							# print "69 att"
							Attente_trame_69('69')
			
		if	STATUS_ERR == False:

			time.sleep(1)

			data65 = RECU_65.split()
			data66 = RECU_66.split()
			data67 = RECU_67.split()
			data68 = RECU_68.split()
			data69 = RECU_69.split()	

			if data65[5] == "65":
				PUB11 =  data65[6:22]
				PUB11 = ''.join(PUB11)
				#print "PUB11:", PUB11
				CLE_P11 = PUB11
			  
			if data66[5] == "66":
				PUB12 =  data66[6:22]
				PUB12 = ''.join(PUB12)
				#print "PUB12:", PUB12
				CLE_P12 = PUB12

			if data67[5] == "67":
				PUB21 =  data67[6:22]
				PUB21 = ''.join(PUB21)
				#print "PUB21:", PUB21
				CLE_P21 = PUB21

			if data68[5] == "68":
				PUB22 =  data68[6:22]
				PUB22 = ''.join(PUB22)
				#print "PUB22:", PUB22
				CLE_P22 = PUB22
				
			if data69[5] == "69":
				PUB69 =  data69[6:22]
				PUB69 = ''.join(PUB69)	
				#print "PUB69_NONCE:", PUB69
				NONCE = PUB69
			
				
		
def SHARED_KEY():

	global CLE_P11
	global CLE_P12
	global CLE_P21
	global CLE_P22
	global SHARED
	
	# #print "cle11", CLE_P11
	# #print "cle12", CLE_P12
	# #print "cle21", CLE_P21
	# #print "cle22", CLE_P22
	
	CLE_1 = CLE_P11 + CLE_P12
	CLE_2 = CLE_P21 + CLE_P22

	# #print "PUB1:", CLE_1	
	# #print "PUB2:", CLE_2
	
	ALICE_X = int(CLE_1, 16)
	ALICE_Y = int(CLE_2, 16)

	# #print "PUB1:", ALICE_X	
	# #print "PUB2:", ALICE_Y		

	bob4_pub = secp256r1(ALICE_X, ALICE_Y)

	alice_ses = bob4_pub * alice_prv
	#print "ALICE_SES", alice_ses

	s7 = str(alice_ses)
	s7 = s7.replace(",", "")
	s7 = s7.replace("(", " ")
	s7 = s7.replace(")", " ")		
	data7 = s7.split()

	SHARED_1 = data7[1]
	#print "SHARED_1", SHARED_1

	#58C930EAB4F0E1997812C2116C828021BB2FD99D24D7DA8E11E96978EEB68EA2
	#58C930EAB4F0E1997812C2116C828021

	SHARED =  SHARED_1[0:32]
	SHARED = ''.join(SHARED)
	#print "SHARED_2", SHARED
				
	
def ASCII_TO_HEX(ASC):

	str = list(ASC)

	for i in range(0,len(str)) :
		str[i] = str[i].encode("hex")
		
	#print "STR", str
	   
def nonce_init():

	global NONCE
	
	NONCE_C = re.findall('..',NONCE)
	##print "NONCE3", NONCE_C[3]
	##print "NONCE2", NONCE_C[2]
	##print "NONCE1", NONCE_C[1]
	##print "NONCE0", NONCE_C[0]
	
	NONCE_C[3] = "00"
	NONCE_C[2] = "00"
	NONCE_C[1] = "00"
	NONCE_C[0] = "00"
	
	NONCE_D = ''.join(NONCE_C)
	#print "NONCED", NONCE_D
	NONCE =  NONCE_D
	
def nonce_increment():

	global NONCE
	
	NONCE_C = re.findall('..',NONCE)
	#print "NONCE23", NONCE_C[3]
	#print "NONCE22", NONCE_C[2]
	#print "NONCE21", NONCE_C[1]
	#print "NONCE20", NONCE_C[0]
	
	DEC3 = int(NONCE_C[3], 16) #1E = 30 dec
	DEC2 = int(NONCE_C[2], 16)
	DEC1 = int(NONCE_C[1], 16)
	DEC0 = int(NONCE_C[0], 16)
		
	if DEC3 == 255:
		DEC3 = 0
		DEC2 = DEC2 + 1
		if DEC2 == 255:
			DEC2 = 0
			DEC1 = DEC1 + 1
			if DEC1 == 255:
				DEC1 = 0
				DEC0 = DEC0 + 1
				if DEC0 == 255:
					DEC0 = 0
					DEC1 = 0
					DEC2 = 0
					DEC3 = 0
	else:
		DEC3 = DEC3 + 1
		
	#print "HEX", "{:02x}".format(DEC3)
	NONCE_C[3] = "{:02x}".format(DEC3)	
	NONCE_C[2] = "{:02x}".format(DEC2)
	NONCE_C[1] = "{:02x}".format(DEC1)
	NONCE_C[0] = "{:02x}".format(DEC0)
	
	##print "DEC3 ", DEC3 
	##print "NONCE2", NONCE_C
	NONCE_D = ''.join(NONCE_C)
	NONCE =  NONCE_D
	#print "NONCE_ENCR", NONCE
	
def crypt():

	global TRAME_VIDE_32
	global TRAME_VIDE_34
	global SHARED
	
	
	TRAME = TRAME_VIDE_32
	
	#print 'KEY: ', SHARED
	KEY = SHARED
	
	key = binascii.unhexlify(KEY)
	IV = binascii.unhexlify('00000000000000000000000000000000')#os.urandom(16) vecteur d'initalisation

	pom1 = binascii.hexlify(key).upper()
	##print "KEY:",
	##print pom1

	pom = binascii.hexlify(IV).upper()
	##print "VI:",
	##print pom
	DATAR = 8
	#Out[6]: b'3C118E12E1677B8F21D4922BE4B2398E'

	encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
	
	text = binascii.unhexlify(NONCE)
	pom2 = binascii.hexlify(text).upper()
	#print "DATA:",
	#print 'POM2', pom2
	ciphertext = encryptor.encrypt(text)

	AES_NONCE = binascii.hexlify(ciphertext).upper() # AES entre la cle et le nonce_increment
	
	#print "NONCE", NONCE
	#print "AES_NONCE", AES_NONCE
					
	#TRAME_S = re.findall('..',TRAME)
	
	AES_NONCE_S = re.findall('..',AES_NONCE)
	
	TRAME_S = TRAME
	DEC1 = TRAME_S     #reserve l espace memoire
	DEC2 = AES_NONCE_S #reserve l espace memoire
	DEC3 = AES_NONCE_S #reserve l espace memoire
	DEC4 = AES_NONCE_S #reserve l espace memoire
	
	TRAME_S = TRAME
	#print "TRAME_S", TRAME_S
	#print "AES_NONCE_S", AES_NONCE_S
	
	for i in range(0,16) : #met la trame au format decimal
		DEC1[i] =  int(TRAME_S[i], 16)
		DEC2[i] =  int(AES_NONCE_S[i], 16)
		
	#print "DEC1" , DEC1
	#print "DEC2" , DEC2
	
	for i in range(0,16) : #met la trame au format decimal
		DEC3[i] =  DEC1[i] ^ DEC2[i]
		DEC4[i] =  "{:02x}".format(DEC3[i])
		
	##print "DEC4" , DEC4
	NONCE_D = ''.join(DEC4)
	TRAME_VIDE_34 = NONCE_D
	#print "TRAME_CHIFFRE", TRAME_VIDE_34
	
	j = 0;
	
	for i in range(0,16):
		 TRAME_VIDE_32[i] = TRAME_VIDE_34[j] + TRAME_VIDE_34[j+1]
		 j = j + 2
	
	#print "TRAME_CHIFFRE32: ", TRAME_VIDE_32
	TRAME_VIDE_32 = ''.join(TRAME_VIDE_32)
	#print "TRAME_CHIFFRE32: ", TRAME_VIDE_32
	
	nonce_increment()
	
def ENVOI_TRAME ():

	global TRAME_VIDE_32
	
	TRAME_VIDE_32 = ''.join(TRAME_VIDE_32)
			
	#print "TRAME_VIDE_32 ENVOI_TRAME", TRAME_VIDE_32
	child.sendline("char-write-cmd 0x0010 " + TRAME_VIDE_32)
	time.sleep(0.1)
	
def WL_Device():

	global DEVICE_ARG
										
	Device_name	= DEVICE_ARG;
	print "WL_DEVICE OK"
			
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
		dataa = json.load(f)	
		 
		 
	if dataa[Device_name]['WL'] == '0': #le device est deja whiteliste
	
		dataa[Device_name]['WL'] = '1'
		with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as f:
			json.dump(dataa, f, indent=2)	
			
def BL_Device():

	global DEVICE_ARG
										
	Device_name	= DEVICE_ARG;
	print "WL_DEVICE NON OK"
			
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
		dataa = json.load(f)	
		 
		 
	if dataa[Device_name]['WL'] == '1': #le device est deja whiteliste
	
		dataa[Device_name]['WL'] = '0'
		with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as f:
			json.dump(dataa, f, indent=2)	
	
	
	
def Recu_32(): # adresse mac de passerelle accepte

	global TRAME_Recue
	global RECU_32
	
	#print '323232323232 RECU!!!!!', TRAME_Recue[0]
	
	if(TRAME_Recue[1] == '01'):
		RECU_32 = True
		print "adresse MAC passerelle OK"
		print "ERREUR = 0"
		STATUS_ERR3 = '00'
	else:
		RECU_32 = False
		print "adresse MAC passerelle non OK"
		print "ERREUR = 1"
		STATUS_ERR3 = '04'

def Recu_41(): # mot de passe recu avec succes

	global TRAME_Recue
	global RECU_41
	#print '414141414 RECU!!!!!', TRAME_Recue[0]
	
	if(TRAME_Recue[1] == '01'):
		RECU_41 = True
		print "MOT de passe recu passerelle OK"
		
		WL_Device()
		
		STATUS_ERR3 = '00'
	else:
		RECU_41 = False
		print "MOT de passe recu passerelle non OK"
		BL_Device()
		STATUS_ERR3 = '05'
	
def Recu_50():

	global TRAME_Recue
	global RECU_50
	#print '505050502 RECU!!!!!', TRAME_Recue[0]
	
	if(TRAME_Recue[1] == '01'):
		RECU_50 = True
		#print "50 bien recu"
	else:
		RECU_50 = False
		#print "50 non recu"
	
def Recu_60():

	global TRAME_Recue
	global RECU_60
	#print '606060606060 RECU!!!!!', TRAME_Recue[0]
	
	if(TRAME_Recue[1] == '01'):
		RECU_60 = True
		print "60 data"
	else:
		RECU_60 = False
		print "60 data"
	
def Recu_B1():

	global TRAME_Recue
	global NB_USER
	
	#print 'B1B1B1B1B1B1RECU!!!!!', TRAME_Recue[0]
	
	NB_USER_HEX = TRAME_Recue[1] 
	#print 'NB_USERS_HEX', NB_USER_HEX
	
	x = int(NB_USER_HEX, 16)
	#print 'NB_USERS', x
	NB_USER = x
	RECU_B1 = True
	
def Recu_B2():

	global TRAME_Recue
	global NB_USER
	global NOM_USER
	global MAC_DEVICE
	
	#print 'B2B2B2B2B22BRECU!!!!!', TRAME_Recue[0]
	
	taille_nom = int(TRAME_Recue[1], 16)
	NOM_USER = ''.join(TRAME_Recue[2:taille_nom + 2])
	NOM_USER = NOM_USER.decode("hex")
	#NOM_USER = NOM_USER.decode("hex").encode("ISO-8859-1")
	#print 'NOM_USER !!!: ', NOM_USER
	NOM_USER = ''.join(TRAME_Recue[2:taille_nom + 2])
		
def Recu_B3():

	global TRAME_Recue
	global MAC_DEVICE
	
	#print 'B3B3B3B3B3B3BBRECU!!!!!', TRAME_Recue[0]
	
	DROIT_USER = TRAME_Recue[8]
	WHITELIST = TRAME_Recue[7]
	MAC_USER = ''.join(TRAME_Recue[1:7])
	
	#print "MAC_USER !!!: ", MAC_USER
	#print "WHITELIST !!!: ", WHITELIST
	#print "DROIT_USER !!!: ", DROIT_USER
	
	USER_name = "USER_" + str(hex_int_8);
	#print "Enregistement OK"
		
	a_dict1 = {USER_name: {'NOM_USER': NOM_USER, 'MAC_USER': MAC_USER, 'WHITELIST': WHITELIST, 'DROIT_USER': DROIT_USER}}

	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json') as f:
		dataa = json.load(f)	
		 
	dataa.update(a_dict1)

	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json', 'w') as f:
		json.dump(dataa, f, indent=2)	

	# with open('data.txt', 'a') as outfile:
    # json.dump(hostDict, outfile, indent=2)
	
def Recu_A1():

	global TRAME_Recue
	global NOM_USER_LOG
	
	#print 'A1A1A1A1A1A1A1A1RECU!!!!!', TRAME_Recue[0]
	
	taille_nom = int(TRAME_Recue[1], 16)
	NOM_USER_LOG = ''.join(TRAME_Recue[2:taille_nom + 2])
	NOM_USER_LOG = NOM_USER_LOG.decode("hex")
	#NOM_USER = NOM_USER.decode("hex").encode("ISO-8859-1")
	#print 'NOM_USER !!!: ', NOM_USER_LOG
	NOM_USER_LOG = ''.join(TRAME_Recue[2:taille_nom + 2])
	
def Recu_A2():

	global TRAME_Recue
	
	global NOM_USER_LOG 
	global MAC_USER_LOG
	global ACTION 
	global DATE_HEURE_LOG
	global MAC_DEVICE
	
	#print 'A2A2A2A2A2A2A2A2RECU!!!!!', TRAME_Recue[0]
	
	ACTION = TRAME_Recue[7]
	DATE_HEURE_LOG = ''.join(TRAME_Recue[8:15])
	MAC_USER_LOG = ''.join(TRAME_Recue[1:7])
	
	#print "ACTION !!!: ", ACTION 
	#print "DATE_HEURE_LOG !!!: ", DATE_HEURE_LOG
	#print "MAC_USER_LOG !!!: ", MAC_USER_LOG
	
	LOG_name = "LOG_" + str(hex_int_8);
	#print "LOG_SAVE OK"
		
	a_dict1 = {LOG_name: {'NOM_USER_LOG': NOM_USER_LOG, 'MAC_USER_LOG': MAC_USER_LOG, 'ACTION': ACTION , 'DATE_HEURE_LOG': DATE_HEURE_LOG}}

	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Logs.json') as f:
		dataa = json.load(f)	
		 
	dataa.update(a_dict1)

	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Logs.json', 'w') as f:
		json.dump(dataa, f, indent=2)	
	
		
def Commutateur():

	global TRAME_VIDE_32
	global TRAME_Recue
	
	TRAME_Recue = re.findall('..', TRAME_VIDE_32)
	
	options = {'32' : Recu_32,
		   '41' : Recu_41,
           '50' : Recu_50,
           '60' : Recu_60,
           'b1' : Recu_B1,
		   'b2' : Recu_B2,
		   'b3' : Recu_B3,
		   'a1' : Recu_A1,
		   'a2' : Recu_A2,
    }
	
	options[TRAME_Recue[0]]()
		
def decrypt():

	global TRAME_VIDE_32
	global TRAME_VIDE_34
	global SHARED
	
	TRAME = TRAME_VIDE_32
	
	#print 'KEY: ', SHARED
	KEY = SHARED
	
	key = binascii.unhexlify(KEY)
	IV = binascii.unhexlify('00000000000000000000000000000000')#os.urandom(16) vecteur d'initalisation

	pom1 = binascii.hexlify(key).upper()
	##print "KEY:",
	##print pom1

	pom = binascii.hexlify(IV).upper()
	##print "VI:",
	##print pom
	DATAR = 8
	#Out[6]: b'3C118E12E1677B8F21D4922BE4B2398E'

	encryptor = AES.new(key, AES.MODE_CBC, IV=IV)
	
	text = binascii.unhexlify(NONCE)
	pom2 = binascii.hexlify(text).upper()
	#print "DATA:",
	#print 'POM2', pom2
	ciphertext = encryptor.encrypt(text)

	AES_NONCE = binascii.hexlify(ciphertext).upper() # AES entre la cle et le nonce_increment
	
	#print "NONCE", NONCE
	#print "AES_NONCE", AES_NONCE
					
	#TRAME_S = re.findall('..',TRAME)
	
	AES_NONCE_S = re.findall('..',AES_NONCE)
	
	TRAME_S = TRAME
	DEC1 = TRAME_S     #reserve l espace memoire
	DEC2 = AES_NONCE_S #reserve l espace memoire
	DEC3 = AES_NONCE_S #reserve l espace memoire
	DEC4 = AES_NONCE_S #reserve l espace memoire
	
	TRAME_S = TRAME
	#print "TRAME_S", TRAME_S
	#print "AES_NONCE_S", AES_NONCE_S
	
	for i in range(0,16) : #met la trame au format decimal
		DEC1[i] =  int(TRAME_S[i], 16)
		DEC2[i] =  int(AES_NONCE_S[i], 16)
		
	#print "DEC1" , DEC1
	#print "DEC2" , DEC2
	
	for i in range(0,16) : #met la trame au format decimal
		DEC3[i] =  DEC1[i] ^ DEC2[i]
		DEC4[i] =  "{:02x}".format(DEC3[i])
		
	##print "DEC4" , DEC4
	NONCE_D = ''.join(DEC4)
	TRAME_VIDE_34 = NONCE_D
	#print "TRAME_CHIFFRE", TRAME_VIDE_34
	
	j = 0;
	
	for i in range(0,16):
		 TRAME_VIDE_32[i] = TRAME_VIDE_34[j] + TRAME_VIDE_34[j+1]
		 j = j + 2
	
	#print "TRAME_CHIFFRE32: ", TRAME_VIDE_32
	TRAME_VIDE_32 = ''.join(TRAME_VIDE_32)
	#print "TRAME_CHIFFRE32_2: ", TRAME_VIDE_32
	
	nonce_increment()
	
	Commutateur()
	
	
	
def ajoutCRC():

	global TRAME_VIDE_32
	FULL_TRAME1 = ''.join(TRAME_VIDE_32[0:16])
	
	#print "FULL_TRAME1", FULL_TRAME1
	
	crc16 = crcmod.mkCrcFun(0x11021,rev=False, initCrc=0xFFFF, xorOut=0x0000)
	CRC_DEC = crc16(FULL_TRAME1.decode("hex"))
	
	#print CRC_DEC
	
	s = struct.pack('>H', CRC_DEC)
	first, second = struct.unpack('>BB', s)
	
	#print first
	#print second
	
	TRAME_VIDE_32 = re.findall('..',FULL_TRAME1)
	
	#print "TAILLE", len(TRAME_VIDE_32)
	
	#print "TRAME_VIDE_32", TRAME_VIDE_32
	
	FIRST = str("{:02x}".format(first))
	SECOND = str("{:02x}".format(second))
	
	#print "FIRST", FIRST
	#print "SECOND", SECOND
	
	TRAME_VIDE_32 = TRAME_VIDE_32 + re.findall('..',FIRST) + re.findall('..',SECOND) + re.findall('..','FF')
	
	FULL_TRAME = ''.join(TRAME_VIDE_32)
	TRAME1 =  FULL_TRAME
	#print "TRAME + CRC", TRAME1
	
	#30526173706265727279000000000000

	# OPCODE = '30'
	# CONTENU = '58C930EAB4F0E3'
	# Montage_Trame(OPCODE, CONTENU)
	# ASCII_TO_HEX(NOM_RPI)
	# MAC_FORMAT (MAC)
	# ENVOI_TRAME()
	#18F4620

def ENVOI_TRAME32 ():
	global TRAME_VIDE_32
	
	child.sendline("char-write-cmd 0x0010 " + TRAME_VIDE_32)
	time.sleep(0.1)


def Deconnexion ():

	time.sleep(1)
	child.sendline("disconnect")
	#print("Disconnect")
	
	time.sleep(2)
	child.sendline("quit")
	#print("Quit")
	
def Chiffrement():
	print("OK")

def Att_Trame(TRAME_RECUE):
	print("OK2")
	
def Montage_Trame(OPCODE, CONTENU): 

   global TRAME_VIDE_32
   global TRAME_VIDE_34
   global TRAME_VIDE_64
   
   RAND_M = binascii.b2a_hex(os.urandom(16))
   TRAME_VIDE_32 = re.findall('..',RAND_M)
   RAND_M2 = TRAME_VIDE_32
   
   #print "CONTENU_1: ",CONTENU
  
   if OPCODE == '30':   #NOM
	   #print "OPCODE 30 CONTENU"
	   TRAME1_S = list(CONTENU)
	   
	   for i in range(0,len(TRAME1_S)) :
			TRAME1_S [i] = TRAME1_S [i].encode("hex")
		
   if OPCODE == '31': #MAC
	   #print "OPCODE 31 CONTENU"
	   TRAME1_S = re.findall('..', CONTENU)
	   
   if (OPCODE == '40') or (OPCODE == '51') or (OPCODE == 'B0') or (OPCODE == 'A0') or (OPCODE == 'B7') or (OPCODE == 'B8'): #mdp
	   #print "OPCODE 40 CONTENU"
	   TRAME1_S = re.findall('..', CONTENU)
   
   #print "TRAME1_S", TRAME1_S
   #print "LEN", len(TRAME1_S)
   
   TRAME2_S = TRAME1_S
   
   #print "TRAME2", TRAME2_S
   
   if len(TRAME2_S) < 16: #a completer rajouter des zeros
		LONG = 16 - len(TRAME2_S)
		lst = RAND_M2[0:LONG]#['00'] * LONG 
		TRAME_VIDE_32 = TRAME2_S + lst
   
   #print "TRAME_VIDE_32_STR", TRAME_VIDE_32
   TRAME_VIDE_32 = (re.findall('..',OPCODE)) + TRAME_VIDE_32 

   if OPCODE == '31':
		TRAME_VIDE_32[7] = '02'       
		
   #print "TRAME_VIDE_32", TRAME_VIDE_32  # ['30', '52', '61', '73', '70', '62', '65', '72', '72', '79', '00', '00', '00', '00', '00']
   #print "LEN", len(TRAME_VIDE_32)  # 16 si tt vas bien
   
   ajoutCRC()
   crypt() # chiffre et incremente le nonce
   #time.sleep(0.2)
   ENVOI_TRAME32()
   
   
def Attente_Trame(OPCODE):

	global NONCE
	global TRAME_VIDE_32
	global STATUS_ERR2
	global PLUS_DE_LOGS

	if (STATUS_ERR2 == False):
	
		j = child.expect(['Notification handle = 0x000d.*', 'Error: .*',pexpect.EOF, pexpect.TIMEOUT], timeout = 5) 
		
		if j == 0: # ok
			# #print 'OK'
			#print("Connexion reussie !")
			connexion_OK = True
			non_connecte = 0
		if j == 1: 
			print 'ERROR!'
			#print child.after
			connexion_OK = False
				
		if j == 2: # EOF
			print 'EOF'
			connexion_OK = False
				
		if j == 3: # timeout
			print 'timeout trame'
			connexion_OK = False

		if connexion_OK == True:

			STATUS_ERR2 = False

			RECU_OP = child.after
			#print RECU_OP
			
			dataOP = RECU_OP.split()
			
			DATAOP1 =  dataOP[5:21]
			DATAOP1 = ''.join(DATAOP1)
			#print "DATAOP1:", DATAOP1
			DATAOP2 = (re.findall('..',DATAOP1))
			#print "DATAOP2:", DATAOP2
			
			TRAME_VIDE_32 = DATAOP2
			#print "TRAME_VIDE_32_decrypt:", TRAME_VIDE_32
			decrypt()
			#print "FIN attente trame"
		else:
			print "ERREUR RECEPTION 1: ", OPCODE
			
			if (OPCODE == 'A1' or OPCODE == 'A2'):
				print "Plus de logs: ", OPCODE
				PLUS_DE_LOGS = True
			
			STATUS_ERR2 = True
	else:
		print "ERREUR RECEPTION 2: ", OPCODE  
		
		if (OPCODE == 'A1' or OPCODE == 'A2'):
			print "Plus de logs:", OPCODE
			PLUS_DE_LOGS = True
			STATUS_ERR2 = False
		
		
def MAC_RPI_RM(): 

	global MAC_RPI
	
	#print "MAC_RPI", MAC_RPI
	MAC_RPI2 = MAC_RPI.replace(":","")
	
	MAC_RPI = MAC_RPI2
	#print "MAC_RPI", MAC_RPI

def Recherche_MAC_USER():

	global USER_MODIF_ARG
	global Test_Presence_User
	global MAC_UTILISATEUR_MODIF
	global MAC_UTILISATEUR_SUPPR
	
	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json') as data_file:    
		jdata = json.load(data_file)
				
	# with open('Save_JSON/SAVE_MP_SERRURE.json') as data_file3:    
		# MOT_J = json.load(data_file3)

	TEST41 = USER_MODIF_ARG
	
	print "USER_MODIF_ARG", TEST41
	
	# MDP = MOT_J['MP']
	#MDP = 'AZERTYUIOP'

	test1 =  TEST41 in jdata
	test2 = False

	if test1 == True:
		#print ("Vrai1")
		test2 =  'MAC_USER' in jdata[TEST41]
	else:
		#EMPTY = 4
		print ("USER non existant")

	if test2 == True:
		print ("Vrai2")
	else:
		print ("Faux2")
		
	if((test1 == True) and (test2 == True)):
		Test_Presence_User = True
		MAC_UTILISATEUR_MODIF = jdata[TEST41]["MAC_USER"]
		MAC_UTILISATEUR_SUPPR = jdata[TEST41]["MAC_USER"]
		print "MAC_UTILISATEUR_MODIF", MAC_UTILISATEUR_MODIF
			
	else:
		Test_Presence_User = False
	
def MAC_RPI_GET():

	global MAC_RPI
	
	proc = subprocess.Popen(["hciconfig -a"], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	#print "program output:", out

	data = out.splitlines()
	s = str(data[1])
	data2 = s.split()
	print "MAC_RPI:", data2[2]
	MAC_RPI = data2[2]
	MAC_RPI_RM()
	
	
def ENVOI_DE_TRAMES1(): 
	
	global NOM_RPI
	global MAC_RPI
	
	global RECU_32
	global RECU_41
	
	global MDP
		 
	Montage_Trame('30', NOM_RPI)# envoi le nom de l'utilisateur
	#MAC_RPI = "000000000000"
	Montage_Trame('31', MAC_RPI) # informe la serrure de l'adresse MAC
	Attente_Trame('32') # accepte ou non la passerelle
	
	if(RECU_32 == True): # passerelle whitelist

		print "MDP" , MDP
		Montage_Trame('40', MDP) # indique le mot de passe de passerelle
		Attente_Trame('41') # mot de passe valide ou non
	
		if(RECU_41 == True): # passerelle mot de passe
			Montage_Trame('51', MAC_RPI) #Demande l'etat de la serrure
			Attente_Trame('50') #Donne l'etat de la serrure
			Attente_Trame('60') #Donne l'etat de la batterie, temporisation et duree de temporisation
	
	
def Ajout_heure_Update_Logs():

	global MAC_DEVICE
	
	Heure_Scan = strftime("%H:%M:%S   %d/%m/%Y", time.localtime())
	DATE_MAX = str(Heure_Scan)
	
	a_dict1 = {"HEURE_UPDATE": {'DATE': DATE_MAX}} 
	
	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Logs.json') as f:
			dataa = json.load(f)	
			 
	dataa.update(a_dict1)
			
	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Logs.json', 'w') as f:
		json.dump(dataa, f, indent=2)		
		
def Ajout_heure_Update_USER():

	global MAC_DEVICE
	
	Heure_Scan = strftime("%H:%M:%S   %d/%m/%Y", time.localtime())
	DATE_MAX = str(Heure_Scan)
	
	a_dict1 = {"HEURE_UPDATE": {'DATE': DATE_MAX}} 
	
	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json') as f:
			dataa = json.load(f)	
			 
	dataa.update(a_dict1)
			
	with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json', 'w') as f:
		json.dump(dataa, f, indent=2)	
			
	

def ENVOI_DE_TRAMES2(): 
	
	global MODE_CONNEXION_1
	global hex_int_8
	global MAC_UTILISATEUR_MODIF
	global DROITS_MODIF
	global MAC_UTILISATEUR_SUPPR
	
	global DEVICE_ARG
	global USER_MODIF_ARG
	global ACTION_ARG
	global DROITS_ARG
	
	global PLUS_DE_LOGS

	global Test_Presence_User
	
	MODE_CONNEXION_1 = ACTION_ARG
	
	if (DROITS_ARG == 'w') or (DROITS_ARG == 'W'): #whitelist
		print 'WL'
		DROITS_MODIF = '01'
		
	if (DROITS_ARG == 'b') or (DROITS_ARG == 'B'): #blacklist
		print 'BL'
		DROITS_MODIF = '00'
	
	if(MODE_CONNEXION_1 == '1'): #0 recupere liste utilisateur
	 
		Trame_VIDE_7 = '00'
		open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json', 'w').close()	
		data8 = {}  

		with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Users.json', 'w') as outfile:  
			json.dump(data8, outfile)
			
		Ajout_heure_Update_USER()
			
		Montage_Trame('B0', Trame_VIDE_7)# envoi le nombre d'utilisateurs
		Attente_Trame('B1')
		
		print "RECEPTION USER !!!!"
		hex_int_8 = int(Trame_VIDE_7[0], 16)
		
		hex_int_8 = hex_int_8 + 1
		FIRST = str("{:02x}".format(hex_int_8))
		
		#print "TRAME1_S0", FIRST
		
		for i in range(0,NB_USER) : #NB_USER
			print "NB_USER OK"
			FIRST = str("{:02x}".format(hex_int_8))
			Montage_Trame('B0', FIRST)
			Attente_Trame('B2')
			Attente_Trame('B3')
			hex_int_8 = hex_int_8 + 1
			
		
		#MODE_CONNEXION_1 = '2' #A ENLEVER !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!		
			
	if(MODE_CONNEXION_1 == '2'): #2 recupere les logs
	 
		Trame_VIDE_7 = '00' #nb de logs a afficher !
		NB_LOGS = 125
		
		open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Logs.json', 'w').close()	
		data8 = {} 
		
		with open('/home/Devismes_Bridge/Equipements/' + MAC_DEVICE + '/Logs.json', 'w') as outfile:  
			json.dump(data8, outfile)
		
		Ajout_heure_Update_Logs()
		print "Chargement en cours..."
		
		#Montage_Trame('B0', Trame_VIDE_7)# envoi le nombre de l'utilisateur
		#Attente_Trame('B1')
		
		#print "RECEPTION USER !!!!"
		hex_int_8 = int(Trame_VIDE_7[0], 16)
		
		hex_int_8 = hex_int_8 + 1
		FIRST = str("{:02x}".format(hex_int_8))
		
		#print "TRAME1_S0", FIRST
				
		for i in range(0,NB_LOGS) : #NB_logs
			
			if(PLUS_DE_LOGS == False):
				print	"OK NB_logs"
				FIRST = str("{:02x}".format(hex_int_8))
				Montage_Trame('A0', FIRST)
				Attente_Trame('A1')
				Attente_Trame('A2')
				hex_int_8 = hex_int_8 + 1
				
			else:
				print "plus de logs"
				break
				
				
			
	if(MODE_CONNEXION_1 == '3'): #3 modifie utilisateur en fonction de son adresse MAC
	 
		Recherche_MAC_USER()
		
		if(Test_Presence_User == True):
		
			CONTENU = DROITS_MODIF + MAC_UTILISATEUR_MODIF
			print "CONTENU 3", CONTENU
			Montage_Trame('B7', CONTENU)# envoi la mac de l'utilisateur

			print "MODE_CONNEXION_1 = 3"
		else:
			print "USER non existant, impossible de le modifier !"
		
		
	if(MODE_CONNEXION_1 == '4'): #4 supprime utilisateur en fonction de son adresse MAC
	  
		Recherche_MAC_USER()
		
		if(Test_Presence_User == True):
		
			CONTENU = MAC_UTILISATEUR_SUPPR
			print CONTENU
			Montage_Trame('B8', CONTENU)# envoi la mac de l'utilisateur

			print "MODE_CONNEXION_1 = 4"
		else:
			print "USER non existant, impossible de le supprimer !"
			
	if(MODE_CONNEXION_1 == '5'): #5 etablit une connexion simple, pas besoin de mot de passe en plus
	
			print "Mode de connexion simple pas de trames supplementaires"

def stock_heure():
	
	date = datetime.datetime.now()
	DATE_MAX = str(date)
	
	print "DATE_MAX", DATE_MAX
	
	
	open('/home/Devismes_Bridge/JSON_List/Last_connected.json', 'w').close()	
	data8 = {}  

	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json', 'w') as outfile:  
		json.dump(data8, outfile)
				
	a_dict1 = {"Heure": {"DATE_MAX": DATE_MAX, "Conn": "1"}}

	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json') as f:
		dataa = json.load(f)	
		 
	dataa.update(a_dict1)

	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json', 'w') as f:
		json.dump(dataa, f, indent=2)	

			
def main():
	
	print("MAIN")
	print "SYS_VER:", (sys.version)

	global STATUS_ERR
	global STATUS_ERR2
	global STATUS_ERR3
	
	stock_heure()
	Arguments()
	# time.sleep(5)
	Charger_Device() #charge le Device scanne en fonction du JSON
	
	if (Test_Presence_Device == True):
		Connexion_Device() #Tente de se connecter au device
	else: 
		print("Equipement inexistant !, Relancez un Scan")
	
	if Device_Connect == True:
		print("Device_Connect = true")
	
		Chiffrement_ECDH()

		if STATUS_ERR == False:  # les trames  65,66,67,68,69 sont bien recues
			SHARED_KEY()
			nonce_init()
			#nonce_increment()
			#print "NONCE_GLOBAL", NONCE
			MAC_RPI_GET()
			
			ENVOI_DE_TRAMES1() #etablit la connexion jusqu'a reception de 60
			#Montage_Trame('30',NOM_RPI)
			
			if STATUS_ERR3 == '00' and RECU_32 == True and RECU_41 == True:

				ENVOI_DE_TRAMES2() #agit en fonction du front end
				Deconnexion()
				
			else:
				if RECU_32 == False:
					STATUS_ERR3 = '04'
					print "STATUS = 4"
					
				if RECU_41 == False and RECU_32 == True:
					STATUS_ERR3 = '05'	
					print "STATUS = 5"

			if STATUS_ERR2 == False and	RECU_32 == True and	RECU_41 == True:
				print "STATUS = 1" # tout s'est deroule correctement
			if STATUS_ERR2 == True and	RECU_32 == True and	RECU_41 == True:
				print "STATUS = 3" # une trame a saute


		else: 
			print "STATUS = 6" #Le chiffrement a echoue

		
if __name__ == "__main__":
    main()
 
 
 
 
	

