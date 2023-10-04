from gameObject import GameObject


class Player(GameObject):
    """Objeto Player

    Args:
        GameObject (GameObject): este objeto, hereda de GameObject.
    """
    def __init__(self, x, y, width, height, image_path, speed):
        """Función constructor del Player

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

    def move(self, direction, max_width, max_height):
        """Función de movimiento del Player

        Args:
            direction (str): Dirección de movimiento del jugador. "L"-Izquierda, "R"-Derecha, "U"-Arriba, "D"-Abajo
            max_width (int): anchura máxima en la que se puede mover el jugador.
            max_height (int): altura máxima en la que se puede mover el jugador.
        """
        if (self.x >= max_width - self.width and direction=="R") or (self.x <= 0 and direction=="L"):
            return
        if (self.y >= max_height- self.height and direction=="D") or (self.y <= 0 and direction=="U"):
            return
        match direction:
            case "R":
                self.x+=self.speed
            case "L":
                self.x-=self.speed
            case "U":
                self.y-=self.speed
            case "D":
                self.y+=self.speed
            case _ :
                pass