import sqlite3
from datetime import date
from datetime import datetime
import os

class gestionBD():
	"""docstring for gestionBD"""

	def __init__(self):
		#Conectamos a la base de datos y la creamos si no existe
		self.miConexion=sqlite3.connect("iphone2pc")
		#Creamos el cursor 
		self.miCursor = self.miConexion.cursor()

	def crearBD(self):
		#get the count of tables with the name
		self.miCursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='OPCIONES_USUARIO' ''')

		#if the count is 1, then table exists
		if self.miCursor.fetchone()[0]==1 : 
			existe = 1
		else:
			#Al meter 3 comillas seguidas, permite dividir la query en varias lineas
			self.miCursor.execute('''
			CREATE TABLE OPCIONES_USUARIO (
			EXT_FOTO_ORIGEN VARCHAR(150),
			EXT_VID_ORIGEN VARCHAR(150),
			RUTA_DESTINO TEXT,
			TIPO_MOVIMIENTO VARCHAR(1),
			FORMATO_SALIDA_FIC VARCHAR(50),
			HEIC2JPG BOOLEAN)
			''')			

			self.miCursor.execute("INSERT INTO OPCIONES_USUARIO VALUES('','','','','',0)")

		#get the count of tables with the name
		self.miCursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='RUTAS_ORIGEN' ''')

		#if the count is 1, then table exists
		if self.miCursor.fetchone()[0]==1 : 
			existe = 1
		else:
			self.miCursor.execute('''
			CREATE TABLE RUTAS_ORIGEN (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			RUTA TEXT)
			''')

			#self.miCursor.execute("INSERT INTO CONFIG VALUES('','','',0,1,1)")

		self.miConexion.commit()
		self.miConexion.close()

	def obtenerDato(self,laTabla,elCampo):
		self.miCursor.execute("SELECT "+elCampo+" FROM " + laTabla)
		return self.miCursor.fetchall()		

	def guardarTextoBase(self,textoR,textoP):
		self.miCursor.execute("UPDATE TEXTOSBASE SET EMAIL=?, WHATSAPP=?",(textoR,textoP))
		self.miConexion.commit()

	def recuperarTextoBase(self):
		self.miCursor.execute("SELECT EMAIL FROM TEXTOSBASE")
		return self.miCursor.fetchall()	

	def insertarRegistro(self,tabla,laPersona):
		#print(laPersona.keys())
		persona=[
		(laPersona['NOMBRE'],laPersona['APELLIDOS'],laPersona['CPOSTAL'],laPersona['DIRECC'],laPersona['TELEFONO'],laPersona['MAIL'],laPersona['NACIMIENTO'],0,0)
		]

		try:
			self.miCursor.executemany("INSERT INTO " +tabla+ " VALUES(NULL,?,?,?,?,?,?,?,?,?)", persona)
			self.miConexion.commit()
		except Exception as ex:
			print(ex)
		


	def cabeceraTabla(self,tabla):
		#Vamos a leer los registros de la tabla
		self.miCursor.execute("SELECT * FROM " +tabla)
		return list(map(lambda x: x[0], self.miCursor.description)) #Con esto sacamos el nombre de los campos de la tabla

	def buscarPersonas(self,tabla,soloCumple,tipoEnvio=None):
		#Vamos a leer los registros de la tabla
		today = date.today()
		mesActu = today.month
		diaActu = today.day
		
		#laConsulta = "SELECT * FROM " +tabla+ " WHERE strftime('%m', NACIMIENTO) = " +str(mesActu)+ " AND strftime('%d', NACIMIENTO) = " + str(diaActu)
		#laConsulta = "SELECT * FROM " +tabla+ " WHERE NOMBRE = ?",(nombre,)

		if soloCumple == 'S':
			self.miCursor.execute("SELECT * FROM " +tabla+ " WHERE CAST(substr(NACIMIENTO,6,2) as INTEGER) = ? AND CAST(substr(NACIMIENTO,1,2) as INTEGER) = ?",(mesActu,diaActu))
		else:
			if tipoEnvio == 'E':
				self.miCursor.execute("SELECT * FROM " +tabla+ " WHERE AVIEMAIL<>0")
			elif tipoEnvio == 'W':
				self.miCursor.execute("SELECT * FROM " +tabla+ " WHERE AVIWHATS<>0")
			else:
				self.miCursor.execute("SELECT * FROM " +tabla)

		#Devolvemos los resultados
		return self.miCursor.fetchall()

	def actuTipoAviso(self,tipoAviso,valor):
		if tipoAviso=='W':
			self.miCursor.execute("UPDATE CONFIG SET AVIWHATS=?",(valor,))
			self.miConexion.commit()
		elif tipoAviso=='E':
			self.miCursor.execute("UPDATE CONFIG SET AVIEMAIL=?",(valor,))
			self.miConexion.commit()

	def checkValorConfig(self,campo,elId):
		try:
			self.miCursor.execute("SELECT "+campo+" FROM PERSONAS WHERE ID=?",(int(elId),))
			#Devolvemos los resultados		
			return self.miCursor.fetchall()
		except:
			return []

	def cambiarDato(self,laTabla,elCampo,elValor,elID):

		#print(laTabla,elCampo,elValor,elID)
		self.miCursor.execute("UPDATE " +laTabla+" SET "+elCampo+"=? WHERE ID=?",(elValor,int(elID)))
		self.miConexion.commit()

	def datosAdmin(self,tabla):
		try:
			self.miCursor.execute("SELECT EMAILADMIN,TLFADMIN FROM CONFIG")
			#Devolvemos los resultados		
			return self.miCursor.fetchall()
		except:
			return []

	def modifValorConfig(self,laTabla,elCampo,elValor):
		self.miCursor.execute("UPDATE " +laTabla+" SET "+elCampo+"=?",(elValor,))
		self.miConexion.commit()