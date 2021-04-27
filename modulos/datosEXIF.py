import locale
import os
#Sacar exif fotos
import exifread
from datetime import datetime
#Sacar geolocalizacion
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import InvalidInputError, RateLimitExceededError, UnknownError
#Sacar datos videos MOV
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

class datosExif(object):
	"""docstring for datosExif"""
	def __init__(self,elArchivo,tipo):
	  locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

	  self.LatGrados= 0
	  self.LonGrados= 0

	  if tipo == 'F':
	  	self.datosExifFotos(elArchivo)
	  elif tipo == 'V':
	  	self.datosExifVideos(elArchivo)


	def datosExifFotos(self,laImagen):
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
	                  self.LatGrados = int(ValGrados)
	              elif (tipoLat == 'S'):
	                  self.LatGrados = int(ValGrados) * -1
	              self.LatMinutos = int(ValMinutos)
	              self.LatSegundos = float(ValSegundos)
	          elif tag == 'GPS GPSLongitude':
	              if tipoLon == 'E':
	                  self.LonGrados = int(ValGrados)
	              elif tipoLon == 'W':
	                  self.LonGrados = int(ValGrados) * -1
	              self.LonMinutos = int(ValMinutos)
	              self.LonSegundos = float(ValSegundos)
	          #Indica que el fichero tiene datos EXIF, si no los tiene, lo mandamos a la carpeta de a revisar
	          tieneExif = 'Si'     
	      elif tag == 'Image DateTime':
	        laFecha = ''
	        laFecha = str(tags[tag])
	        self.elMes = datetime.strptime(laFecha[:10], "%Y:%m:%d").strftime('%Y - %B')
	        #Indica que el fichero tiene datos EXIF, si no los tiene, lo mandamos a la carpeta de a revisar
	        tieneExif = 'Si'
	  if tieneExif == 'No' or self.LatGrados== 0 or self.LonGrados== 0:
	    self.elMes='FotosArevisar'
	    self.elPueblo='Todos'
	  else:
	    self.sacarUbicacion()



	def datosExifVideos(self,elVideo):
	  parser = createParser(elVideo)
	  metadata = extractMetadata(parser)

	  laFecha = ''
	  laFecha = str(metadata.get('creation_date'))
	  parser.close()
	  self.elMes = datetime.strptime(laFecha[:10], "%Y-%m-%d").strftime('%Y - %B')  
	  self.elPueblo='Videos'  

	def sacarUbicacion(self):
	  key = 'd10cf63d329b4c158a1cd23baf90dc4a'
	  geocoder = OpenCageGeocode(key)
	  # Latitude & Longitude input
	  Latitude = self.convertirGrados2Decimal(self.LatGrados,self.LatMinutos,self.LatSegundos)
	  Longitude = self.convertirGrados2Decimal(self.LonGrados,self.LonMinutos,self.LonSegundos)
	  try:
	    results = geocoder.reverse_geocode(Latitude, Longitude, language='es', no_annotations='1')
	    dicComp = {}
	    dicComp =  results[0]['components']
	    if dicComp and len(dicComp):
	      try:
	        self.elPueblo = dicComp['town']
	      except:
	        try:
	          self.elPueblo = dicComp['municipality']
	        except:
	          try:
	            self.elPueblo = dicComp['village']
	          except:
	            try:
	              self.elPueblo = dicComp['city']
	            except:
	              self.elPueblo = 'Sin Datos'

	  except RateLimitExceededError as ex:
	    print(ex)
	    # Your rate limit has expired. It will reset to 2500 next day
	  except InvalidInputError as ex:
	    # this happens for example with invalid unicode in the input data
	    print(ex)  

	def convertirGrados2Decimal(self,losGrados,losMinutos,losSegundos):
	    grados   = losGrados
	    minutos  = losMinutos
	    segundos = losSegundos
	    if grados >= 0:
	        valDec = (segundos/3600) + (minutos/60) + grados
	    else:
	        valDec = - (segundos/3600) - (minutos/60) + grados
	    return str(valDec)  
