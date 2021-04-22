# A simple setup script to create an executable using PyQt5. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt5app.py is a very simple type of PyQt5 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

build_exe_options = {"include_files": ["modulos","gui"],
                     "includes":['atexit','PyQt5'],
                    }    

#options = {"build_exe": {"includes": "atexit"}"include_files": {"include_files": "modulos/datosEXIF.py,modulos/conexionBD.py,modulos/recogerFicheros.py,gui/master.ui"}}

executables = [Executable("master.py", base=base)]
'''
build_exe_options = {"include_files": {"modulos/datosEXIF.py,modulos/conexionBD.py,modulos/recogerFicheros.py,gui/master.ui"}}

setup(
    name="Movil2Pc",
    version="1.0",
    description="Aplicacion para ordenar fotos de tus moviles",
    options=options,
    executables=executables,
)
'''
setup(
    name="Movil2Pc",
    version="1.0",
    description="Aplicacion para ordenar fotos de tus moviles",
    options={"build_exe":build_exe_options},
    executables=executables,
)