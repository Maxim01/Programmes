#!/usr/bin/env python
# -*-coding:Latin-1 -*

import smtplib
import json
import subprocess
import re
import os
import os.path

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import sys
import time
from time import gmtime, strftime

DEVICE_ARG = "VIDE"
Alarme_type_ARG = "VIDE"
ALRM = 'VIDE'
message_alarme = "message_alarme"
fromaddr = "VIDE"
password = "VIDE"
toaddr = "VIDE"

ARGUMENT_ARG = "VIDE"

def Arguments():

	global DEVICE_ARG
	global Alarme_type_ARG

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	if (len(sys.argv) == 3):
		DEVICE_ARG = sys.argv[1]
		Alarme_type_ARG = sys.argv[2]
		
	if (len(sys.argv) == 2):
		Alarme_type_ARG = sys.argv[1]

def type_alarme():

	global Alarme_type_ARG
	global ALRM
	
	if (Alarme_type_ARG == '1'): 
		ALRM = 'Choc sur la porte'
		montage_mail()
		envoi_mail()
		
	if (Alarme_type_ARG == '3'): 
		montage_mail2()
		envoi_mail()
		
		
def montage_mail():

	global DEVICE_ARG
	global message_alarme
	global ALRM
	
	Heure_Scan1 = strftime("%H:%M:%S ", time.localtime())
	Heure_Scan2 = strftime("%d-%m-%Y ", time.localtime())
	
	message_alarme = 'Une alarme à été déclenchée sur votre serrure "' + DEVICE_ARG + '" à ' + Heure_Scan1 + 'le ' + Heure_Scan2 + '\n' + 'Alarme de type: ' + ALRM
	print	message_alarme
	
def montage_mail2():

	global DEVICE_ARG
	global message_alarme
	global ALRM
	
	Heure_Scan1 = strftime("%H:%M:%S ", time.localtime())
	Heure_Scan2 = strftime("%d-%m-%Y ", time.localtime())
	
	message_alarme = 'E-mail de test envoyé depuis votre passerelle connectée Devismes à ' + Heure_Scan1 + 'le ' + Heure_Scan2
	print	message_alarme
			
	
def recup_mail():

	global fromaddr
	global password
	global toaddr
	
	with open('/home/Devismes_Bridge/JSON_List/mail.json') as f:
		dataa = json.load(f)	
		
	print "OK1"	
	fromaddr = dataa['mail']['adresse'] 
	toaddr= dataa['mail']['Dest']
	password = dataa['mail']['MP']
	
	process = subprocess.Popen("sudo python /home/Devismes_Bridge/Programmes/compteur_serrure.py 9", shell=True, stdout=subprocess.PIPE)
	process.wait()
	(out, err) = process.communicate()
	Data_Scan = out.splitlines()
	
	#print "LEN", len(Data_Scan)
	#print Data_Scan
	MP1 = Data_Scan[16].split(":")
	
	password = MP1[1]
	
	print "PSWD", password
		

def envoi_mail():

	global message_alarme
	global fromaddr
	global password
	global toaddr
	
	#fromaddr="projetdevismes@gmail.com"
	#password="devismes2017"

	#toaddr="maxime.f80@gmail.com"

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Alarme serrure - Devismes"
	 
	body = message_alarme
	msg.attach(MIMEText(body, 'plain'))
	 
	server = smtplib.SMTP_SSL('smtp.gmail.com:465')
	server.ehlo()
	server.login(fromaddr, password)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	
def Creation_Dossier_Device():
	
	file_path = "/home/Devismes_Bridge/JSON_List/mail.json"
		
	if not os.path.exists(file_path):
		print "EXIST Device = Create"
		file1 = open('/home/Devismes_Bridge/JSON_List/mail.json', 'w+')
		file1.write('{"mail": {"Dest": "VIDE", "adresse": "VIDE", "MP": "VIDE"}}')
	else:
		print "EXIST Device = OK"

		
def main():

	print("MAIN")
	print "SYS_VER:", (sys.version)
	
	Arguments()
	Creation_Dossier_Device()
	recup_mail()
	type_alarme()
	

if __name__ == "__main__":
    main()