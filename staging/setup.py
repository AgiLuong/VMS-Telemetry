from cx_Freeze import setup, Executable

base = None    

executables = [Executable("initialize.py", base=base)]

packages = ["numpy", "os", "pyqtgraph", "glob","gmplot","ctypes","numpy","struct","signal","digi"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Telemetry_App",
    options = options,
    version = "2.0",
    description = 'Vroom Vroom',
    executables = executables
)
