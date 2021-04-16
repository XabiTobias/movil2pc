import os

def convertirHEIC():
  for dirpath,dirs,files in os.walk('C:\\Users\\Xabi\\Documents\\ProyectosPython\\iphone2pc\\fotosNuevas\\2021 - abril\\Gorliz'):
    for file in files:
      if file.upper().endswith((".HEIC")):
        fotoOriginal = '"' + os.path.join(dirpath, file) + '[0]"'
        fotoR = '"' + os.path.join(dirpath, file[:-5]) + '.jpg"'
        print("Convirtiendo {} en -> {}".format(fotoOriginal,fotoR))
        stream = os.popen('"C:\\Program Files\\ImageMagick-7.0.11-Q16-HDRI\\magick" ' + fotoOriginal + ' ' + fotoR)
        output = stream.read()

convertirHEIC()