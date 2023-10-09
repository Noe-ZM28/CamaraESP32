from cx_Freeze import setup, Executable

# Lista de módulos que deseas incluir en el ejecutable
modules = [
    'datetime', 'escpos', 'qrcode', 'tkinter', 're', 'time', 'PIL', 'PIL.ImageTk', 'pymysql', 'random', 'qrcode', 'xlsxwriter', 'serial'
]

# Archivo principal de tu proyecto (donde se encuentra el punto de entrada)
main_script = 'main.py'

# Configuración para generar el ejecutable
setup(
    name='COBRO - PASE',
    version='1.0',
    description='Sistema de control de acceso vehicular',
    options={
        'build_exe': {
            'packages': modules,
        },
    },
    executables=[
        Executable(script=main_script)
    ]
)
