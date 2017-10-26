#!/usr/bin/env python
# -*-coding:Latin-1 -*

import smtplib
import json
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

def Arguments():

	global DEVICE_ARG
	global Alarme_type_ARG

	print "Arguments: ", sys.argv
	print "NB d'arguments: ", len(sys.argv)
	
	if (len(sys.argv) == 3):
		DEVICE_ARG = sys.argv[1]
		Alarme_type_ARG = sys.argv[2]

def type_alarme():

	global Alarme_type_ARG
	global ALRM
	
	if (Alarme_type_ARG == '1'): 
		ALRM = 'Choc sur la porte'
		
def montage_mail():

	global DEVICE_ARG
	global message_alarme
	global ALRM
	
	Heure_Scan1 = strftime("%H:%M:%S ", time.localtime())
	Heure_Scan2 = strftime("%d-%m-%Y ", time.localtime())
	
	message_alarme = 'Une alarme à été déclenchée sur votre serrure "' + DEVICE_ARG + '" à ' + Heure_Scan1 + 'le ' + Heure_Scan2 + '\n' + 'Alarme de type: ' + ALRM
	print	message_alarme
			
	
def recup_mail():

	global fromaddr
	global password
	
	with open('/home/Devismes_Bridge/JSON_List/mail.json') as f:
		dataa = json.load(f)	
		
	print "OK"	
	fromaddr = dataa['mail']['adresse'] 
	password = dataa['mail']['MP']
	toaddr= dataa['mail']['Dest']
		

	
def envoi_mail():

	global message_alarme
	global fromaddr
	global password
	
	#fromaddr="projetdevismes@gmail.com"
	#password="devismes2017"

	toaddr="maxime.f80@gmail.com"

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
	
def main():

	print("MAIN")
	print "SYS_VER:", (sys.version)
	
	Arguments()
	type_alarme()
	recup_mail()
	montage_mail()
	envoi_mail()

		
if __name__ == "__main__":
    main()