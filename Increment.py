import json
import time
import subprocess

# def increment():
										
		# with open('/home/Devismes_Bridge/JSON_List/INC.json') as f:
			# dataa = json.load(f)	
			 
		# increm = dataa['1']['INC'] + 1
		
		# dataa['1']['INC'] = increm
		
		# with open('/home/Devismes_Bridge/JSON_List/INC.json', 'w') as f:
			# json.dump(dataa, f, indent=2)	




def main():
	
	while (1):
		print("Restart SCAN !")
		proc = subprocess.Popen(["sudo python /home/Devismes_Bridge/Programmes/Scan_BLE.py"], stdout=subprocess.PIPE, shell=True)
		time.sleep(10)
		


		
if __name__ == "__main__":
    main()
 