import time
import pygame
import pygame_menu
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
        self.white_colour = (255, 255, 255)
        
        # Fuente de texto
        pygame.font.init()
        self.my_font = pygame.font.SysFont("inkfree", 26, bold=True)

        # Creamos la pantalla
        self.game_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.game_window.get_width()
        self.height = self.game_window.get_height()
        # Creamos un GameObject para el fondo de la pantalla
        self.background = GameObject(0, 0, self.width, self.height, 'assets/background3.jpg') 

        # Reproducir musica en bucle
        pygame.mixer.init()
        self.musica=pygame.mixer.music.load("assets/doctorwho.mp3")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)

        # Creamos el GameObject objetivo
        self.goal= GameObject(int(self.width/2.5), 20, 200, 90, 'assets/blackhole.png') 
        self.level=1 # Nivel
        self.points=0 # Puntuacion
        self.name="Desconocido"

        with open('record.txt') as f:
            record = f.readlines()
        self.high_score=int(record[1])
        self.high_scorer=record[0].rstrip()

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

        text_surface = self.my_font.render(f"Torreznos: {str(self.points)}", False, self.white_colour)
        self.game_window.blit(text_surface, (15,0))

        records = self.my_font.render("High-score:", False, self.white_colour)
        records2= self.my_font.render(f"{self.high_scorer}, {str(self.high_score)} agujeros negros", False, self.white_colour)
        self.game_window.blit(records, (self.width-175,0))
        self.game_window.blit(records2, (self.width-records2.get_width(),30))

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
        #Record de puntuacion
        if self.points>self.high_score:
            self.high_scorer=self.name
            self.high_score=self.points
            with open('record.txt', 'w') as f:
                f.write(f"{self.name[:12]}\n")
                f.write(f"{str(self.points)}")

        # Colocamos un objeto de juego Player en la posición de inicio
        width_player=10+int(self.level*16)
        height_player=15+int(self.level*25)
        self.player = Player(random.randint(0,self.game_window.get_height()), self.height-height_player, width_player, height_player, 'assets/tardis.png', 10)
        # La velocidad de movimiento de los enemigos varia segun el nivel en el que estamos
        speed = 3 + (self.level * 3)

        # Creamos los enemigos según nivel
        if self.level >= 4.0:
            self.enemies = [
                Enemy(400, random.randint(151,self.game_window.get_height()-self.player.height-100), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed+random.randint(0,2)),
                Enemy(400, random.randint(151,self.game_window.get_height()-self.player.height-100), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed+random.randint(0,2)),
                Enemy(400, random.randint(151,self.game_window.get_height()-self.player.height-100), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed+random.randint(0,2)),
            ]
        elif self.level >= 2.0:
            self.enemies = [
                Enemy(400, random.randint(151,self.game_window.get_height()-self.player.height-100), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed+random.randint(0,2)),
                Enemy(400, random.randint(151,self.game_window.get_height()-self.player.height-100), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed+random.randint(0,2))
            ]
        else:
            self.enemies = [
                Enemy(400, random.randint(151,self.game_window.get_height()-self.player.height-100), random.randint(70,150), random.randint(60,90), 'assets/enemy.png', speed)
            ]

    def check_if_collided(self) -> bool:
        """Función para detectar colisiones con los enemigos y la meta.

        Returns:
            bool: devuelve False si no hay colisión, True si hay colisión.
        """
        for enemy in self.enemies:
            if self.detect_collision(self.player, enemy):
                self.level = 1.0
                self.points = 0
                return True
        if self.detect_collision(self.player, self.goal):
            self.level += 0.5
            self.points +=1
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

    def run_menu(self):
        menu = pygame_menu.Menu('Doctor Who: Across the Universe', 500, 400,
                       theme=pygame_menu.themes.THEME_SOLARIZED)
        
        menu.add.label("¡El Doctor te necesita!\n Lleva la TARDIS al agujero negro para escapar del peligro\nEsquiva las naves Dalek o perderás", max_char=-1, font_size=20)
        menu.add.vertical_margin(15)
        self.name_input=menu.add.text_input('Player: ', default='Desconocido')
        menu.add.button('Play', self.run_game_loop)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        menu.mainloop(self.game_window)

    def run_game_loop(self):
        """Funcion de juego. Es un bucle que se ejecuta 60 veces por segundo, en el cual se actualizan los eventos de pulsación de teclas, la lógica, la pantalla y las colisiones del juego.
        """
        self.name=self.name_input.get_value()
        player_direction = None
        while True:
            # Deteccion de eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
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
                time.sleep(0.5)             
                self.reset_map()

            self.clock.tick(60)

