import json
import time
import subprocess

HEURE_SCAN = 0

def stock_heure():
	
	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json') as f:
		dataa = json.load(f)	
		 
	dataa["Heure"]["Conn"] = 0

	with open('/home/Devismes_Bridge/JSON_List/Last_connected.json', 'w') as f:
		json.dump(dataa, f, indent=2)

def main():
	
	while (1):
		print("Restart SCAN !")
		HEURE_SCAN = HEURE_SCAN + 1
		
		if HEURE_SCAN >= 90 : #1 fois par heure redonne le droit de ractualiser la liste tt les quart d'heure
			stock_heure()
			HEURE_SCAN = 0
		
		proc = subprocess.Popen(["sudo python /home/Devismes_Bridge/Programmes/Scan_BLE.py"], stdout=subprocess.PIPE, shell=True)
		time.sleep(10)
		
		


		
if __name__ == "__main__":
    main()
 