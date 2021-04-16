from smb.SMBConnection import SMBConnection
#Sacar datos videos MOV
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from datetime import datetime

rutaOriginal = 'zuri/Photos/MobileBackup/iPhone de Zuri'
listaCarpetas = []
listaArchivos = []
encuentraCarpeta = True

usuario = 'xabitsu'
password = 'xabier08'
server = 'XabiStation'

conexion = SMBConnection(usuario, password, server, server)
conexion.connect(server)
results = conexion.listPath('Homes', rutaOriginal)

def datosExifVideos(elVideo):
  parser = createParser(elVideo)
  metadata = extractMetadata(parser)

  laFecha = ''
  laFecha = str(metadata.get('creation_date'))
  elMes = datetime.strptime(laFecha[:10], "%Y-%m-%d").strftime('%Y - %B') 
  print(laFecha)

def busqueda(nombre):
	print(nombre)
	results2 = conexion.listPath('Homes', nombre)
	for x in results2:
		if x.isDirectory==True: # Es una carpeta
			if x.filename not in('.','..'):
				rutaConsulta = nombre + '/' + x.filename
				print(x.filename)
				listaCarpetas.append(rutaConsulta)
				busqueda(rutaConsulta)
				encuentraCarpeta = True
		else: #Es un fichero
			if x.filename[-3:] == 'mov':
				listaArchivos.append(nombre + '/' + x.filename)	

for x in results:
	if x.isDirectory==True: # Es una carpeta
		if x.filename not in('.','..'):
			rutaConsulta = rutaOriginal + '/' + x.filename
			listaCarpetas.append(rutaConsulta)
			busqueda(rutaConsulta)
			encuentraCarpeta = True
	else: #Es un fichero
		listaArchivos.append(x.filename)	

#print("Carpetas: ", listaCarpetas)
#print("Ficheros: ", listaArchivos)
for elemento in listaArchivos:
	print("Fichero: ", elemento)
	datosExifVideos('//xabistation/homes/' + elemento)