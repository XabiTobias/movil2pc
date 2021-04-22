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
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog,QMainWindow, QApplication, QMessageBox, QFileDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

#-----------------------------------------------------------------#
#-------------Creamos las funciones para el master----------------#
#-----------------------------------------------------------------#
def crearCarpeta(ubi1,ubi2):
  #Sacamos la ruta destino de las fotos
  gestionarBD = gestionBD()
  for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
    for ele_rutaD2 in ele_rutaD:
      elDestinoR = ele_rutaD2 
  laCarpeta = elDestinoR + '/' + ubi1 + '/' + ubi2
  makedirs(laCarpeta, exist_ok=True)
  return laCarpeta

def convertirHEIC():
  gestionarBD = gestionBD()
  for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
    for ele_rutaD2 in ele_rutaD:
      elDestinoR = ele_rutaD2 

  for dirpath,dirs,files in os.walk(elDestinoR):
    for file in files:
      if file.upper().endswith((".HEIC")):
        fotoOriginal = os.path.join(dirpath, file)       
        fotoRe = file[:-5] + '.jpg'
        fotoR = os.path.join(dirpath, fotoRe)
        #print("Convirtiendo {} en -> {}".format(fotoOriginal,fotoR))
        #Insertamos en el log el movimiento del fichero
        textoLog = "Convirtiendo {} con extensión HEIC en -> {}".format(fotoOriginal,fotoR)
        insertarLog(textoLog)
        stream = os.popen('"C:\\Program Files\\ImageMagick-7.0.11-Q16-HDRI\\magick" "' + fotoOriginal + '" "' + fotoR + '"')
        output = stream.read()
        if os.path.exists(fotoOriginal):
          try:
            os.remove(fotoOriginal) # one file at a time
            textoLog = "Borrado el fichero {}".format(fotoOriginal,)
          except Exception as e:
            textoLog = 'Error en el borrado del fichero HEIC : '+str(e)
          insertarLog(textoLog)

def insertarLog(textoLog):
  file = open("log\\log.txt", "a+")
  file.write(textoLog + '\n')
  file.close()
         
#---------------------------   FIN   -----------------------------#
#-------------Creamos las funciones para el master----------------#
#-----------------------------------------------------------------#


#-----------------------------------------------------------------#
#-----------------Parte grafica de la pantalla--------------------#
#-----------------------------------------------------------------#
class ventanaPrincipal(QMainWindow):
  """docstring for ClassName"""
  def __init__(self):
    super().__init__()
    uic.loadUi("gui/master.ui",self)

    gestionarBD = gestionBD()

    #Caracteristicas pantallas
    # set the title 
    self.setWindowTitle("Movil 2 pc") 
    # setting window icon 
    #self.setWindowIcon(QIcon("gui/icono.ico"))      
    # setting icon text 
    #self.setWindowIconText("icono") 

    self.setFixedSize(870, 480)

    ## REMOVE TITLE BAR
    self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    self.frameOptEntrada.show()
    self.frameOptSalida.hide()
    self.frameOptLanzar.hide()

    self.lblAjustesOk.setHidden(True)

    '''
    #Acciones menu archivo
    self.act_crearBD.triggered.connect(self.crearBD)
    self.act_borrarBD.triggered.connect(self.borrarBD)
    self.ventanaDatosAdmin = ventanaDatosAdmin()
    self.act_datosAdmin.triggered.connect(self.datosAdmin)
    self.act_salir.triggered.connect(self.salirAPP)
    #Acciones menu opciones parte 1
    self.act_xls2bd.triggered.connect(self.xls2bd)
    self.act_bd2xls.triggered.connect(self.bd2xls)
    #Acciones menu opciones parte 2
    self.act_txtadmin.triggered.connect(self.cumplesDia)
    self.act_txtcumple.triggered.connect(self.emailCumple)  
    #Acciones menu cumpleañeros
    self.ventanaCumpleaneros = VentanaCumpleaneros()
    self.act_cumpleaneros.triggered.connect(self.listCumpleaneros)  
    #Acciones menu ayuda
    self.act_acercaDe.triggered.connect(self.acercaDe)  
    '''
    #Acciones cabecera minimizar,maximizar,cerrar
    self.cabMinimizar.clicked.connect(lambda: self.showMinimized())
    self.cabMaximizar.clicked.connect(lambda: self.showMaximized())
    self.cabCerrar.clicked.connect(lambda: self.close())   
    #Acciones botones lateral
    self.btn_ajuEntrada.clicked.connect(self.mostrarV1)
    self.btn_ajuSalida.clicked.connect(self.mostrarV2)
    self.btn_lanzarProceso.clicked.connect(self.mostrarV3)
    self.btn_log.clicked.connect(self.mostrarLog)
    #Acciones pestaña 1
    for elemento in gestionarBD.obtenerDato('RUTAS_ORIGEN','RUTA'):
      for elemento2 in elemento:
        self.rutaOrigen.setText(elemento2)  

    for extension in gestionarBD.extensionesFotoVid('foto'):
      self.extFotos.setText(self.extFotos.text() + extension + ',')
    self.extFotos.setText(self.extFotos.text()[:-1])
    for extension in gestionarBD.extensionesFotoVid('video'):
      self.extVideos.setText(self.extVideos.text() + extension + ',')
    self.extVideos.setText(self.extVideos.text()[:-1])    

    self.btnBuscarCOri.clicked.connect(self.buscarCarpetaOri)     

    self.btnGuardarOri.clicked.connect(self.guardarOri) 
    #Acciones pestaña 2
    for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
      for ele_rutaD2 in ele_rutaD:
        self.rutaDestino.setText(ele_rutaD2) 

    for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','TIPO_MOVIMIENTO'):
      for ele_rutaD2 in ele_rutaD:
        self.cmbMovimiento.setCurrentText(ele_rutaD2)    

    for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','HEIC2JPG'):
      for ele_rutaD2 in ele_rutaD:
        valHEIC = ele_rutaD2
    if valHEIC > 0:
      self.chkHeic.setCheckState(QtCore.Qt.Checked)
    else:
      self.chkHeic.setCheckState(QtCore.Qt.Unchecked)

    self.btnGuardarSal.clicked.connect(self.guardarSal)   
    self.btnBuscarCDes.clicked.connect(self.buscarCarpetaDes)   
    #Acciones pestaña 3
    self.btnStart.clicked.connect(self.lanzarProceso) 
    self.btnVerFotos.clicked.connect(self.verFotos)   
    self.btnVerFotos.setVisible(False)

  def mostrarV1(self):
    self.frameOptEntrada.show()
    self.frameOptSalida.hide()
    self.frameOptLanzar.hide()
  def mostrarV2(self):
    self.frameOptEntrada.hide()
    self.frameOptLanzar.hide()
    self.frameOptSalida.show()
  def mostrarV3(self):
    self.frameOptLanzar.show()
    self.frameOptEntrada.hide()
    self.frameOptSalida.hide()    

  def buscarCarpetaDes(self):
    dialog = QFileDialog()
    self.rutaDestino.setText(dialog.getExistingDirectory(self, 'Selecciona un directorio'))
  def buscarCarpetaOri(self):
    dialog = QFileDialog()
    self.rutaOrigen.setText(dialog.getExistingDirectory(self, 'Selecciona un directorio'))        

  def mostrarLog(self):
    subprocess.run(["notepad","log/log.txt"])

  def guardarOri(self):
    gestionarBD = gestionBD()
    #Ext fotos
    gestionarBD.guardarDato('OPCIONES_USUARIO','EXT_FOTO_ORIGEN',self.extFotos.text())  
    #Ext videos
    gestionarBD.guardarDato('OPCIONES_USUARIO','EXT_VID_ORIGEN',self.extVideos.text())  
    #Ruta
    gestionarBD.guardarDato('RUTAS_ORIGEN','RUTA',self.rutaOrigen.text())  
    #Mostrar label guardados
    #self.lblAjustesOk.setGeometry(QRect(160, 190, 251, 71))
    '''
    try:
      timer = QTimer
      timer.timeout.connect(self.ocultarT)
      timer.start(1000)
    except Exception as e:
      print('Error en el proceso de mover archivo : '+str(e))
    
    try:
      QTimer.singleShot(3000,self.ocultarT())
    except Exception as e:
      print('Error en el proceso de mover archivo : '+str(e))
    #self.lblAjustesOk.setHidden(False)
    '''
  def ocultarT(self):
    self.lblAjustesOk.setHidden(False)

  def guardarSal(self):
    gestionarBD = gestionBD()
    #Ruta destino
    gestionarBD.guardarDato('OPCIONES_USUARIO','RUTA_DESTINO',self.rutaDestino.text())  
    #Copiar o mover
    gestionarBD.guardarDato('OPCIONES_USUARIO','TIPO_MOVIMIENTO',self.cmbMovimiento.currentText())     
    #Convertir HEIC a Jpg
    if self.chkHeic.checkState() > 0:
      elValor = 1
    else:
      elValor = 0 
    gestionarBD.guardarDato('OPCIONES_USUARIO','HEIC2JPG',elValor)  

  def verFotos(self):
    gestionarBD = gestionBD()
    for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','RUTA_DESTINO'):
      for ele_rutaD2 in ele_rutaD:
        path = ele_rutaD2
    subprocess.Popen(f'explorer {os.path.realpath(path)}')

  def lanzarProceso(self):
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

        if(tipoMovimiento =='Copiar'): #Copiar
          try:          
            shutil.copy2(elFicheroCompleto, elDestinoR)
            textoLog = "Fichero {} copiado en carpeta -> {}".format(elemento['nombre'],elDestinoR)
          except Exception as e:
            print('Error en el proceso de copia : '+str(e))
            textoLog = 'Error en el proceso de copia : '+str(e)
        elif(tipoMovimiento=='Mover'): # Mover
          try:       
            shutil.move(elFicheroCompleto, elDestinoR)
            textoLog = "Fichero {} movido a carpeta -> {}".format(elemento['nombre'],elDestinoR)
          except Exception as e:
            print('Error en el proceso de mover archivo : '+str(e))
            textoLog = 'Error en el proceso de mover archivo : '+str(e)
        #Insertamos en el log el movimiento del fichero
        insertarLog(textoLog)
    #Convertir ficheros copiados con formato HEIC a Jpg
    for ele_rutaD in gestionarBD.obtenerDato('OPCIONES_USUARIO','HEIC2JPG'):
      for ele_rutaD2 in ele_rutaD:
        valHEIC = ele_rutaD2
    if valHEIC > 0:
      time.sleep(2)
      convertirHEIC()
    self.btnVerFotos.setVisible(True)
   
#---------------------------   FIN   -----------------------------#
#-----------------Parte grafica de la pantalla--------------------#
#-----------------------------------------------------------------#

#C:\Users\Xabi\Documents\ProyectosPython\movil2pc\gui>pyrcc5 -o ../resources.py images/imagenes.qrc
if __name__ == '__main__':

  app = QApplication(sys.argv)
  gui = ventanaPrincipal()
  gui.show()  
  sys.exit(app.exec_()) 

  '''
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
  '''



