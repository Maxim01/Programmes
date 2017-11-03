import json
import sys

from twilio.rest import Client

SID = "VIDE"
token = "VIDE"
numero_envoi = "VIDE"
numero_reception = "VIDE"

ACTION_ARG = "VIDE"
Message_envoi = "VIDE"

def arguments():

	global ACTION_ARG
	global SID
	global token
	global numero_envoi
	global numero_reception
	global Message_envoi
		
	if ((len(sys.argv) == 4) and (sys.argv[1] == '1')): 
	
			print "programme sid et token"
			ACTION_ARG = sys.argv[1]
			SID = sys.argv[2]
			token = sys.argv[3]
			
	if ((len(sys.argv) == 3) and (sys.argv[1] == '2')): #numero d'envoi
	
			print "programme numero envoi"
			ACTION_ARG = sys.argv[1]
			numero_envoi = sys.argv[2]
			
	if ((len(sys.argv) == 3) and (sys.argv[1] == '3')): #numero de reception
	
			print "programme numero reception"
			ACTION_ARG = sys.argv[1]
			numero_reception = sys.argv[2]
			
	if ((len(sys.argv) == 3) and (sys.argv[1] == '4')): #envoi du message
	
			print "Envoi_SMS"
			ACTION_ARG = sys.argv[1]
			Message_envoi = sys.argv[2]
							
def envoi_sms():

	global SID
	global token
	global numero_envoi
	global numero_reception
	global Message_envoi
	
	print "ENVOI en cours"
	account_sid = SID #"AC672f63c89ea69fb97c91c66a68216576" # Your Account SID from twilio.com/console
	auth_token  = token #"cdad8a674f646e2b4a4b509de28902af"   # Your Auth Token from twilio.com/console
	
	numero_reception1 = numero_reception
	numero_envoi1 = numero_envoi
	Message_envoi1 = Message_envoi
	
	client = Client(account_sid, auth_token)

	message = client.messages.create(to = numero_reception1, from_= numero_envoi1, body = Message_envoi1)

	print(message.sid)

def save_numero_envoi():

	global numero_envoi
	
	print "numero_envoi"
	
	with open("/home/Devismes_Bridge/JSON_List/mail.json") as f:
			dataa = json.load(f)	
			
	dataa["mail"]["num_envoi"] =  numero_envoi
			
	with open("/home/Devismes_Bridge/JSON_List/mail.json", 'w') as f:
			json.dump(dataa, f, indent=2)
			
def save_numero_recep():

	global numero_reception
	
	print "numero_recep"
	
	with open("/home/Devismes_Bridge/JSON_List/mail.json") as f:
			dataa = json.load(f)	
			
	dataa["mail"]["num_recep"] = numero_reception
			
	with open("/home/Devismes_Bridge/JSON_List/mail.json", 'w') as f:
			json.dump(dataa, f, indent=2)
			
def save_SID():

	global SID
	global token
	
	print "SID_Token"
	
	with open("/home/Devismes_Bridge/JSON_List/mail.json") as f:
			dataa = json.load(f)	
			
	dataa["mail"]["sid"] = SID
	dataa["mail"]["token"] = token
			
	with open("/home/Devismes_Bridge/JSON_List/mail.json", 'w') as f:
			json.dump(dataa, f, indent=2)
			
def charge_login():

	global SID
	global token
	global numero_envoi
	global numero_reception
	
	print "Charge login"
	
	with open("/home/Devismes_Bridge/JSON_List/mail.json") as f:
			dataa = json.load(f)	
			
	SID = dataa["mail"]["sid"] 
	token = dataa["mail"]["token"]
	numero_envoi = dataa["mail"]["num_envoi"]
	numero_reception = dataa["mail"]["num_recep"]
			

	
def commutateur():

	global ACTION_ARG
	global SID
	global token
	global numero_envoi
	global numero_reception
	global Message_envoi
	
	if ACTION_ARG == '1':
		save_SID()
		
	if ACTION_ARG == '2':
		save_numero_envoi()
	
	if ACTION_ARG == '3':
		save_numero_recep()
		
	if ACTION_ARG == '4':
		charge_login()
		envoi_sms()


def main():
	
	print("MAIN")
	print "SYS_VER:", (sys.version)
	
	arguments()
	commutateur()
	
	

if __name__ == "__main__":
    main()