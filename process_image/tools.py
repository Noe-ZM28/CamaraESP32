from os import path, listdir

class Tools:
    def __init__(self):pass

    def validate_image(self, path_image):
        # Obtener la extensión del archivo
        _, ext = path.splitext(path_image)

        # Lista de extensiones de imagen comunes (puedes ampliarla según tus necesidades)
        list_ext = ['.jpg', '.png']

        # Verificar si la extensión está en la lista de extensiones de imagen y si la ruta es un archivo y existe
        return True if ext.lower() in list_ext and path.isfile(path_image) else False

    def list_images(self, path_image_dir:str = "./img/plates") -> list:
        list_images = []
        for file in listdir(path_image_dir):
            file_name_complete = path.join(path.abspath(path_image_dir), file)
            if self.validate_image(file_name_complete):
                list_images.append(file_name_complete)

        return list_images
