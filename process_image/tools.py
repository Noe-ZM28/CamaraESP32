from os import path

class Tools:
    def __init__(self):pass

    def validate_image(self, path_image):
        # Obtener la extensión del archivo
        _, ext = path.splitext(path_image)

        # Lista de extensiones de imagen comunes (puedes ampliarla según tus necesidades)
        list_ext = ['.jpg']

        # Verificar si la extensión está en la lista de extensiones de imagen y si la ruta es un archivo y existe
        return True if ext.lower() in list_ext and path.isfile(path_image) else False

