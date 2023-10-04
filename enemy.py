from gameObject import GameObject


class Enemy(GameObject):
    """Objeto Enemy

    Args:
        GameObject (GameObject): este objeto, hereda de GameObject.
    """
    def __init__(self, x, y, width, height, image_path, speed):
        """Función constructor del Enemy

        Args:
            x (int): posición en el eje x
            y (int): posición en el eje y
            width (int): anchura del objeto
            height (int: altura del objeto
            image_path (str): ruta de la imagen del objeto
            speed (float): velocidad de movimiento
        """
        super().__init__(x, y, width, height, image_path)

        self.speed = speed

    def move(self, max_width):
        """Función de movimiento del Enemy

        Args:
            max_width (int): anchura máxima en la que se puede mover el jugador.
        """
        if self.x <= 0:
            self.speed = abs(self.speed)
        elif self.x >= max_width - self.width:
            self.speed = -self.speed
        self.x += self.speed