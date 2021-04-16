#Sacar exif fotos
import exifread
#Sacar datos videos MOV
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
#Sqlite
from modulos.conexionBD import * #mysqli

import locale
import time
import subprocess, sys
import json
from recogerFicheros import gravJson
from datetime import datetime
#Sacar geolocalizacion
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
#Movimiento de carpetas y ficheros
import os
from os import makedirs
#Esto permite copiar ficheros
import shutil

elMes = ''
elPueblo = ''
LatGrados = 0
LatMinutos = 0
LatSegundos = 0
LonGrados = 0 
LonMinutos = 0
LonSegundos  = 0

def crearCarpeta(ubi1,ubi2):
  laCarpeta = 'fotosNuevasXabi/' + ubi1 + '/' + ubi2
  makedirs(laCarpeta, exist_ok=True)
  return laCarpeta

def convertirGrados2Decimal(losGrados,losMinutos,losSegundos):
    grados   = losGrados
    minutos  = losMinutos
    segundos = losSegundos
    if grados >= 0:
        valDec = (segundos/3600) + (minutos/60) + grados
    else:
        valDec = - (segundos/3600) - (minutos/60) + grados
    return str(valDec)

def sacarUbicacion(LatGradosf,LatMinutosf,LatSegundosf,LonGradosf,LonMinutosf,LonSegundosf):
  key = 'd10cf63d329b4c158a1cd23baf90dc4a'
  geocoder = OpenCageGeocode(key)
  # Latitude & Longitude input
  Latitude = convertirGrados2Decimal(LatGradosf,LatMinutosf,LatSegundosf)
  Longitude = convertirGrados2Decimal(LonGradosf,LonMinutosf,LonSegundosf)
  global elPueblo
  try:
    results = geocoder.reverse_geocode(Latitude, Longitude, language='es', no_annotations='1')
    dicComp = {}
    dicComp =  results[0]['components']
    if dicComp and len(dicComp):
      try:
        elPueblo = dicComp['town']
      except:
        try:
          elPueblo = dicComp['municipality']
        except:
          try:
            elPueblo = dicComp['village']
          except:
            try:
              elPueblo = dicComp['city']
            except:
              elPueblo = 'Sin Datos'

  except RateLimitExceededError as ex:
    print(ex)
    # Your rate limit has expired. It will reset to 2500 next day
  except InvalidInputError as ex:
    # this happens for example with invalid unicode in the input data
    print(ex)    

def datosExifFotos(laImagen):
  global elMes
  global elPueblo
  global LatGrados,LatMinutos,LatSegundos,LonGrados,LonMinutos,LonSegundos

  LatGrados = 0
  LatMinutos = 0
  LatSegundos = 0
  LonGrados = 0 
  LonMinutos = 0
  LonSegundos  = 0
  locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))
  # Open image file for reading (binary mode)
  f = open(laImagen, 'rb')

  filepath=laImagen
  size=round(os.path.getsize(filepath)/(1024*1024),2)
  #print(str(size) + ' Mbytes')
  # Return Exif tags
  tags = exifread.process_file(f)
  tieneExif = 'No'
  for tag in tags.keys():
      if tag  in ('GPS GPSLatitude', 'GPS GPSLongitude', 'GPS GPSLatitudeRef', 'GPS GPSLongitudeRef'):
          temp_string = str(tags[tag])
          separador = ","
          separado = temp_string.split(separador)
          contNum = 1
          contNumSeg = 1
          for s in separado:
              if contNum == 1:
                  ValGrados = s[1:]
              elif contNum == 2:
                  ValMinutos = s
              elif contNum == 3:
                  separador = "/"
                  numSegundos = s.split(separador)
                  if s.count("/") == 0:
                    ValSegundos = s[:-1]
                  else:
                    for s2 in numSegundos:
                        if contNumSeg == 1:
                            ValSeg1 = s2
                        elif contNumSeg == 2:
                            topeSeg2 = len(s2) - 1
                            ValSeg2 = s2[:topeSeg2]
                        contNumSeg = contNumSeg + 1    
                    ValSegundos = int(ValSeg1) / int(ValSeg2)
              contNum = contNum + 1


          if tag == 'GPS GPSLatitudeRef':
              tipoLat = str(tags[tag])
          elif tag == 'GPS GPSLongitudeRef':
              tipoLon = str(tags[tag])

          elif tag == 'GPS GPSLatitude':
              if (tipoLat == 'N'):
                  LatGrados = int(ValGrados)
              elif (tipoLat == 'S'):
                  LatGrados = int(ValGrados) * -1
              LatMinutos = int(ValMinutos)
              LatSegundos = float(ValSegundos)
          elif tag == 'GPS GPSLongitude':
              if tipoLon == 'E':
                  LonGrados = int(ValGrados)
              elif tipoLon == 'W':
                  LonGrados = int(ValGrados) * -1
              LonMinutos = int(ValMinutos)
              LonSegundos = float(ValSegundos)

      elif tag == 'Image DateTime':
          laFecha = ''
          laFecha = str(tags[tag])
          elMes = datetime.strptime(laFecha[:10], "%Y:%m:%d").strftime('%Y - %B')
      #Indica que el fichero tiene datos EXIF, si no los tiene, lo mandamos a la carpeta de a revisar
      tieneExif = 'Si'
  if tieneExif == 'No' or LatGrados== 0 or LonGrados== 0:
    elMes='FotosArevisar'
    elPueblo='Todos'
  else:
    sacarUbicacion(LatGrados,LatMinutos,LatSegundos,LonGrados,LonMinutos,LonSegundos)

def datosExifVideos(elVideo):
  parser = createParser(elVideo)
  metadata = extractMetadata(parser)

  laFecha = ''
  laFecha = str(metadata.get('creation_date'))
  elMes = datetime.strptime(laFecha[:10], "%Y-%m-%d").strftime('%Y - %B')    

def convertirHEIC():
  for dirpath,dirs,files in os.walk('C:\\Users\\Xabi\\Documents\\ProyectosPython\\iphone2pc\\fotosNuevasXabi'):
    for file in files:
      if file.upper().endswith((".HEIC")):
        fotoOriginal = os.path.join(dirpath, file)
        fotoR = file[:-5] + '.jpg'
        print("Convirtiendo {} en -> {}".format(fotoOriginal,fotoR))
        stream = os.popen('"C:\\Program Files\\ImageMagick-7.0.11-Q16-HDRI\\magick" ' + fotoOriginal + ' ' + fotoR)
        output = stream.read()

def insertarLog(textoLog):
  file = open("log\\log.txt", "a")
  file.write(textoLog + os.linesep)
  file.close()        


if __name__ == '__main__':
  gestionarBD = gestionBD()
  gestionarBD.crearBD()
  gravJson()
  makedirs("log/", exist_ok=True)
  file = open("log\\log.txt", "w")

  gestionarBD = gestionBD()
  #Sacar extensiones de fotos y videos seleccionadas por el usuario 
  print(gestionarBD.extensionesFotoVid('foto'))
  print(gestionarBD.extensionesFotoVid('video'))

  #Sacamos el tipo de movimiento, copiar o mover
  for ele_ext in gestionarBD.obtenerDato('OPCIONES_USUARIO','TIPO_MOVIMIENTO'):
    for ele_ext2 in ele_ext:
      tipoMovimiento = ele_ext2 
  #Sacamos la ruta destino de las fotos
  for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
    for ele_rutaD2 in ele_rutaD:
      elDestinoR = ele_rutaD2 

  with open('ficherosaTratar.json') as file:
    data = json.load(file)
    for elemento in data['ficheros']:
      elFicheroCompleto = elemento['ruta'] + '\\' + elemento['nombre']
      #elDestino = 'fotosNuevasXabi'
      makedirs(elDestinoR, exist_ok=True)
      if(tipoMovimiento =='C'): #Copiar
        insertarLog("Fichero {} copiado en carpeta -> {}".format(elemento['nombre'],elDestinoR))
        shutil.copy2(elFicheroCompleto, elDestinoR)
      elif(tipoMovimiento=='M'): # Mover
        insertarLog("Fichero {} movido a carpeta -> {}".format(elemento['nombre'],elDestinoR))   
        shutil.move(elFicheroCompleto, elDestino, copy_function=copy2)
  '''
  with open('ficherosaTratar.json') as file:
    data = json.load(file)
    for elemento in data['ficheros']:
      elFicheroCompleto = elemento['ruta'] + '\\' + elemento['nombre']
      if elemento['extension'].upper() not in ('.MOV','.MP4'):
        print("Fichero tratado -> {}".format(elemento['nombre'],))
        #Sacamos los datos exif de la foto para obtener fecha y Ubicacion
        datosExifFotos(elFicheroCompleto)
        #Creamos la carpeta con formato 2021 - Febrero/ Basauri
        elDestino = crearCarpeta(elMes,elPueblo)
      else:
        datosExifVideos(elFicheroCompleto)    
        elDestino = crearCarpeta('Videos',elMes)
      try:
        #Copiamos el fichero en la nueva carpeta creada
        shutil.copy(elFicheroCompleto, elDestino)
        print("Fichero {} copiado en carpeta -> {}".format(elemento['nombre'],elDestino))       
        print('---------------')
      except Exception as e:
          print('Error Message : '+str(e))
  '''


  print("----")
  #convertirHEIC()



