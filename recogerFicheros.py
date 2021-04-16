import json
import os
import os.path
#Sqlite
from modulos.conexionBD import * #mysqli

def gravJson():
	rutOri = []
	extFotoVid = []
	tuplaExtensiones = ()
	gestionarBD = gestionBD()
	for elemento in gestionarBD.obtenerDato('RUTAS_ORIGEN','RUTA'):
		for elemento2 in elemento:
			rutOri.append(elemento2)

	for ele_ext in gestionarBD.obtenerDato('OPCIONES_USUARIO','EXT_FOTO_ORIGEN'):
		for ele_ext2 in ele_ext:
			extFotoVid.append(ele_ext2)
			separador = ","	
			listaExt = ele_ext2.split(separador)	
	for ele_ext in gestionarBD.obtenerDato('OPCIONES_USUARIO','EXT_VID_ORIGEN'):
		for ele_ext2 in ele_ext:
			extFotoVid.append(ele_ext2)	
			separador = ","	
			listaExt = listaExt + ele_ext2.split(separador)	
	tuplaExtensiones = tuple(listaExt)
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
				if file.upper().endswith(tuplaExtensiones):
					data['ficheros'].append({
						'nombre': file,
						'ruta': root,
						'extension': os.path.splitext(file)[1]})

		with open('ficherosaTratar.json', 'w') as file:
			json.dump(data, file, indent=4)	

if __name__ == '__main__':
	gravJson()	