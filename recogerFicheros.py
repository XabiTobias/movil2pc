import json
import os
import os.path
#Sqlite
from modulos.conexionBD import * #mysqli

def gravJson():
	rutOri = []
	gestionarBD = gestionBD()
	for elemento in gestionarBD.obtenerDato('RUTAS_ORIGEN','RUTA'):
		for elemento2 in elemento:
			rutOri.append(elemento2)
	#Inicializamos variables
	losFicheros = []
	path=''
	data = {}
	data['ficheros'] = []
	#RutaFotosZuriNas = '//xabistation/homes/zuri/Photos/MobileBackup/'
	#RutaFotosXabiNas = '//xabistation/homes/xabitsu/Photos/MobileBackup/Galaxy S10 de Xabier/DCIM/Camera'
	for elPath in rutOri:
		for root,dirs,files in os.walk(elPath):
			for file in files:
				if file.upper().endswith((".HEIC",".JPG","JPEG",".MOV",".MP4")):
					data['ficheros'].append({
						'nombre': file,
						'ruta': root,
						'extension': os.path.splitext(file)[1]})

		with open('data.json', 'w') as file:
			json.dump(data, file, indent=4)	

if __name__ == '__main__':
	gravJson()	