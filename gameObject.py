import pygame


class GameObject:
    """Elemento del juego genérico
    """
    def __init__(self, x, y, width, height, image_path):
        """Constructor del elemento de juego

        Args:
            x (int): posición en el eje x
            y (int): posición en el eje y
            width (int): anchura del objeto
            height (int: altura del objeto
            image_path (str): ruta de la imagen del objeto
        """
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (width, height))

        self.x = x
        self.y = y
        self.width = width
        self.height = height