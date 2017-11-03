import json
import time
import subprocess
from time import gmtime, strftime

HEURE_SCAN = 0

		
def stock_heure2():
	
	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json') as f:
		dataa = json.load(f)	
	

	dataa["Heure_ref"]["DATE_MAX"] = strftime("%H:%M:%S   %d/%m/%Y", time.localtime())
	
	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json', 'w') as f:
		json.dump(dataa, f, indent=2)
	
	
	with open('/home/Devismes_Bridge/JSON_List/Devices.json') as f:
		dataa = json.load(f)	
	
	print "longueur: " ,len(dataa)
	
	if len(dataa) != 0:
		print "len diff 0"
		for i in range(1,len(dataa)+1):
			NOM = "Device_"+ str(i)
			print NOM
			dataa[NOM]["LOG_CONN"] = "0"
			dataa[NOM]["USER_CONN"] = "0"
			
			with open('/home/Devismes_Bridge/JSON_List/Devices.json', 'w') as f:
				json.dump(dataa, f, indent=2)

def main():
	
	global HEURE_SCAN
	
	while (1):
		print("Restart SCAN !")
		HEURE_SCAN = HEURE_SCAN + 1 #toutes les 2 heures
		
		if HEURE_SCAN >= 360 : #1 fois par heure redonne le droit de ractualiser la liste tt les quart d'heure
			print("RAZ_Connexion")
			stock_heure2()
			HEURE_SCAN = 0
		
		proc = subprocess.Popen(["sudo python /home/Devismes_Bridge/Programmes/Scan_BLE.py"], stdout=subprocess.PIPE, shell=True)
		time.sleep(10)
		
		


		
if __name__ == "__main__":
    main()
 