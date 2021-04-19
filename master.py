#Sqlite
from modulos.conexionBD import * #mysqli
#Sacar datos EXIF
from modulos.datosEXIF import *
#Obtener ficheros en un json
from modulos.recogerFicheros import *
import json
#Esto permite copiar ficheros
import shutil
#Movimiento de carpetas y ficheros
import os
from os import makedirs
#Imports mas genericos
import locale
import time
import subprocess, sys
from datetime import datetime
#Imports para GUI
import resources


#-----------------------------------------------------------------#
#-------------Creamos las funciones para el master----------------#
#-----------------------------------------------------------------#
def crearCarpeta(ubi1,ubi2):
  #Sacamos la ruta destino de las fotos
  for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
    for ele_rutaD2 in ele_rutaD:
      elDestinoR = ele_rutaD2 
  laCarpeta = elDestinoR + '/' + ubi1 + '/' + ubi2
  makedirs(laCarpeta, exist_ok=True)
  return laCarpeta

def convertirHEIC():
  for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
    for ele_rutaD2 in ele_rutaD:
      elDestinoR = ele_rutaD2 

  for dirpath,dirs,files in os.walk(elDestinoR):
    for file in files:
      if file.upper().endswith((".HEIC")):
        fotoOriginal = os.path.join(dirpath, file)
        fotoRe = file[:-5] + '.jpg'
        fotoR = os.path.join(dirpath, fotoRe)
        print("Convirtiendo {} en -> {}".format(fotoOriginal,fotoR))
        stream = os.popen('"C:\\Program Files\\ImageMagick-7.0.11-Q16-HDRI\\magick" "' + fotoOriginal + '" "' + fotoR + '"')
        output = stream.read()

def insertarLog(textoLog):
  file = open("log\\log.txt", "a")
  file.write(textoLog + os.linesep)
  file.close()        
#---------------------------   FIN   -----------------------------#
#-------------Creamos las funciones para el master----------------#
#-----------------------------------------------------------------#



if __name__ == '__main__':
  gestionarBD = gestionBD()
  gestionarBD.crearBD()
  gravJson()
  makedirs("log/", exist_ok=True)
  file = open("log\\log.txt", "w")
  locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
  now = str(time.strftime("%c"))
  cabeceraLog= '--------------------------------------'
  cabeceraLog+= '----------' + now + '------------'
  cabeceraLog+= '--------------------------------------'
  insertarLog(cabeceraLog)

  gestionarBD = gestionBD()

  #Sacamos el tipo de movimiento, copiar o mover
  for ele_ext in gestionarBD.obtenerDato('OPCIONES_USUARIO','TIPO_MOVIMIENTO'):
    for ele_ext2 in ele_ext:
      tipoMovimiento = ele_ext2 


  with open('ficherosaTratar.json') as file:
    data = json.load(file)
    for elemento in data['ficheros']:
      elFicheroCompleto = elemento['ruta'] + '\\' + elemento['nombre']
      if elemento['extension'].upper() in gestionarBD.extensionesFotoVid('foto'):
        datExif = datosExif(elFicheroCompleto,'F')
      elif elemento['extension'].upper() in gestionarBD.extensionesFotoVid('video'):
        datExif = datosExif(elFicheroCompleto,'V')

      #Creamos la carpeta con formato 2021 - Febrero/ Basauri
      elDestinoR = crearCarpeta(datExif.elMes,datExif.elPueblo)
      #Lanzamos el proceso que copia o mueve los ficheros a la nueva ruta
      textoLog = ''
      if(tipoMovimiento =='C'): #Copiar
        try:          
          shutil.copy2(elFicheroCompleto, elDestinoR)
          textoLog = "Fichero {} copiado en carpeta -> {}".format(elemento['nombre'],elDestinoR)
        except Exception as e:
          print('Error en el proceso de copia : '+str(e))
          textoLog = 'Error en el proceso de copia : '+str(e)
      elif(tipoMovimiento=='M'): # Mover
        try:         
          shutil.move(elFicheroCompleto, elDestino, copy_function=copy2)
          textoLog = "Fichero {} movido a carpeta -> {}".format(elemento['nombre'],elDestinoR)
        except Exception as e:
          print('Error en el proceso de mover archivo : '+str(e))
          textoLog = 'Error en el proceso de mover archivo : '+str(e)
      #Insertamos en el log el movimiento del fichero
      insertarLog(textoLog)
      #Convertir ficheros copiados con formato HEIC a Jpg
      convertirHEIC()



