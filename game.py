import pygame
from enemy import Enemy
from gameObject import GameObject
from player import Player
import random

class Game:
    """La clase Game es la que se encarga de controlar los aspectos del juego como actualización de pantalla, movimiento, sonido, lógica del juego
    """
    def __init__(self):
        """Clase constructor del juego
        """
        # Altura y anchura de la pantalla de juego
        self.width = 800
        self.height = 1000
        self.white_colour = (255, 255, 255)

        # Creamos la pantalla
        self.game_window = pygame.display.set_mode((self.width, self.height))
        # Creamos un GameObject para el fondo de la pantalla
        self.background = GameObject(0, 0, self.width, self.height, 'assets/background3.jpg') 

        # Reproducir musica en bucle
        pygame.mixer.init()
        self.musica=pygame.mixer.music.load("assets/doctorwho.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        # Creamos el GameObject objetivo
        self.goal= GameObject(325, 20, 150, 90, 'assets/blackhole.png') 
        self.level=1 # Nivel
        self.reset_map() # Reseteamos el mapa
        
        # Cogemos el reloj de pygame para la actualización del juego cada 60 ticks.
        self.clock = pygame.time.Clock() 
    
    def draw_objects(self):
        """Funcion para actualizar la imagen en pantalla de los elementos, tales como fondo de pantalla, jugador, enemigo y objetivo.
        """

        self.game_window.fill(self.white_colour)

        self.game_window.blit(self.background.image, (self.background.x, self.background.y))
        self.game_window.blit(self.goal.image, (self.goal.x, self.goal.y))
        self.game_window.blit(self.player.image, (self.player.x, self.player.y))

        for enemy in self.enemies:
           self.game_window.blit(enemy.image, (enemy.x, enemy.y)) 

        pygame.display.update()
    
    def move_objects(self, player_direction: str):
        """Funcion que se encarga de actualizar el movimiento de los objetos que se mueven (jugador y enemigo)

        Args:
            player_direction (str): Describe la dirección de movimiento del jugador en la pantalla. "L"-Izquierda, "R"-Derecha, "U"-Arriba, "D"-Abajo
        """
        self.player.move(player_direction, self.width, self.height)
        for enemy in self.enemies:
            enemy.move(self.width)
    
    def reset_map(self):
        """Funcion para resetear el mapa cada vez que comienza un nivel. Coloca al jugador en posición de salida y a los enemigos en una posición aleatoria.
        """
        # Colocamos un objeto de juego Player en la posición de inicio
        self.player = Player(550, self.height-150, 100, 150, 'assets/tardis.png', 10)
        # La velocidad de movimiento de los enemigos varia segun el nivel en el que estamos
        speed = 3 + (self.level * 3)

        # Creamos los enemigos según nivel
        if self.level >= 4.0:
            self.enemies = [
                Enemy(400, random.randint(151,400), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed),
                Enemy(400, random.randint(151,400), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed),
                Enemy(400, random.randint(151,400), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed),
            ]
        elif self.level >= 2.0:
            self.enemies = [
                Enemy(400, random.randint(151,400), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed),
                Enemy(400, random.randint(151,400), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed)
            ]
        else:
            self.enemies = [
                Enemy(400, random.randint(151,400), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed)
            ]

    def check_if_collided(self) -> bool:
        """Función para detectar colisiones con los enemigos y la meta.

        Returns:
            bool: devuelve False si no hay colisión, True si hay colisión.
        """
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level = 1.0
                return True
        if self.detect_collision(self.player, self.goal):
            self.level += 0.5
            return True
        
        return False


    def detect_collision(self, object_1, object_2) -> bool:
        """Deteccion de colisiones entre dos objetos.

        Args:
            object_1 (GameObject): objeto de juego 1 (Player, Enemy, GameObject)
            object_2 (GameObject): objeto de juego 2 (Player, Enemy, GameObject)

        Returns:
            bool: devuelve False si no hay colisión, True si hay colisión.
        """
        if object_1.y > (object_2.y + object_2.height):
            return False
        elif (object_1.y + object_1.height) < object_2.y:
            return False
        if object_1.x > (object_2.x + object_2.width):
            return False
        elif (object_1.x + object_1.width) < object_2.x:
            return False
        return True

    def run_game_loop(self):
        """Funcion de juego. Es un bucle que se ejecuta 60 veces por segundo, en el cual se actualizan los eventos de pulsación de teclas, la lógica, la pantalla y las colisiones del juego.
        """
        player_direction = None
        while True:
            # Deteccion de eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player_direction = "R"
                    elif event.key == pygame.K_LEFT:
                        player_direction = "L"
                    elif event.key == pygame.K_UP:
                        player_direction = "U"
                    elif event.key == pygame.K_DOWN:
                        player_direction = "D"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player_direction = None

            # Logica del juego
            self.move_objects(player_direction)

            # Actualizar pantalla
            self.draw_objects()
            
            # Colisiones
            if self.check_if_collided():
                self.reset_map()

            self.clock.tick(60)

