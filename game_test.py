import pygame

from face_controller import FaceController, expression_to_command


# ============================================================
# INICIAR PYGAME
# ============================================================

pygame.init()


# ============================================================
# CONFIGURACIÓN DE LA VENTANA
# ============================================================

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Emotion Maze"
)


# ============================================================
# FONDO
# ============================================================

background = pygame.image.load(
    "assets/background.jpg"
).convert()

background = pygame.transform.smoothscale(
    background,
    (WIDTH, HEIGHT)
)


# ============================================================
# CONFIGURACIÓN DEL JUGADOR
# ============================================================

player_size = 90

player_x = WIDTH // 2
player_y = HEIGHT // 2

# Velocidad de movimiento
# 3 = movimiento moderado
player_speed = 3


# ============================================================
# COLOR DE LA INTERFAZ
# ============================================================

COLOR_BLANCO = (255, 255, 255)


# ============================================================
# FUENTE PIXEL
# ============================================================

# Si tienen una fuente pixel instalada en assets/fonts,
# pueden colocarla aquí:
#
# assets/fonts/PressStart2P-Regular.ttf
#
# Si no existe, se utiliza Courier New como respaldo.

FONT_PATH = "assets/fonts/PressStart2P-Regular.ttf"

try:

    font = pygame.font.Font(
        FONT_PATH,
        22
    )

except:

    font = pygame.font.SysFont(
        "Courier New",
        22,
        bold=True
    )


# ============================================================
# CARGAR SPRITES
# ============================================================

def load_sprite(path, height=90):

    image = pygame.image.load(
        path
    ).convert_alpha()

    original_width, original_height = image.get_size()

    scale = height / original_height

    new_width = int(
        original_width * scale
    )

    new_height = int(
        original_height * scale
    )

    image = pygame.transform.smoothscale(
        image,
        (new_width, new_height)
    )

    return image


# ============================================================
# SPRITE NEUTRAL
# ============================================================

neutral_sprite = load_sprite(
    "assets/cat_avatar/neutral/idle.png"
)


# ============================================================
# ANIMACIONES
# ============================================================

animations = {

    "UP": [

        load_sprite(
            "assets/cat_avatar/up/frame_1.png"
        ),

        load_sprite(
            "assets/cat_avatar/up/frame_2.png"
        ),

        load_sprite(
            "assets/cat_avatar/up/frame_3.png"
        ),

        load_sprite(
            "assets/cat_avatar/up/frame_4.png"
        )

    ],

    "DOWN": [

        load_sprite(
            "assets/cat_avatar/down/frame_1.png"
        ),

        load_sprite(
            "assets/cat_avatar/down/frame_2.png"
        ),

        load_sprite(
            "assets/cat_avatar/down/frame_3.png"
        ),

        load_sprite(
            "assets/cat_avatar/down/frame_4.png"
        )

    ],

    "LEFT": [

        load_sprite(
            "assets/cat_avatar/left/frame_1.png"
        ),

        load_sprite(
            "assets/cat_avatar/left/frame_2.png"
        ),

        load_sprite(
            "assets/cat_avatar/left/frame_3.png"
        ),

        load_sprite(
            "assets/cat_avatar/left/frame_4.png"
        )

    ],

    "RIGHT": [

        load_sprite(
            "assets/cat_avatar/right/frame_1.png"
        ),

        load_sprite(
            "assets/cat_avatar/right/frame_2.png"
        ),

        load_sprite(
            "assets/cat_avatar/right/frame_3.png"
        ),

        load_sprite(
            "assets/cat_avatar/right/frame_4.png"
        )

    ]

}


# ============================================================
# SPRITE ACTUAL
# ============================================================

player_image = neutral_sprite


# ============================================================
# CONTROLADOR FACIAL
# ============================================================

controller = FaceController(
    camera_index=1
)


# ============================================================
# RELOJ
# ============================================================

clock = pygame.time.Clock()


# ============================================================
# CONTROL DE ANIMACIÓN
# ============================================================

current_direction = None

animation_frame = 0

animation_timer = 0

# Menor número = animación más rápida
animation_speed = 5


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

running = True

while running:

    # ========================================================
    # EVENTOS DE PYGAME
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    # ========================================================
    # LEER EXPRESIÓN FACIAL
    # ========================================================

    expression, camera_frame = controller.get_expression()


    # ========================================================
    # CONVERTIR EXPRESIÓN EN COMANDO
    # ========================================================

    if expression is not None:

        command = expression_to_command(
            expression
        )

    else:

        command = None


    # ========================================================
    # MOVIMIENTO CONTINUO
    # ========================================================

    # Si existe un comando, el personaje se mueve
    # MIENTRAS el usuario mantenga la expresión.

    if command is not None:

        # ----------------------------------------------------
        # CAMBIO DE DIRECCIÓN
        # ----------------------------------------------------

        if command != current_direction:

            current_direction = command

            animation_frame = 0

            animation_timer = 0


        # ----------------------------------------------------
        # DERECHA
        # ----------------------------------------------------

        if command == "RIGHT":

            player_x += player_speed


        # ----------------------------------------------------
        # IZQUIERDA
        # ----------------------------------------------------

        elif command == "LEFT":

            player_x -= player_speed


        # ----------------------------------------------------
        # ARRIBA
        # ----------------------------------------------------

        elif command == "UP":

            player_y -= player_speed


        # ----------------------------------------------------
        # ABAJO
        # ----------------------------------------------------

        elif command == "DOWN":

            player_y += player_speed


    # ========================================================
    # NEUTRAL / SIN COMANDO
    # ========================================================

    else:

        # Detener completamente al personaje

        current_direction = None

        animation_frame = 0

        animation_timer = 0

        player_image = neutral_sprite


    # ========================================================
    # ANIMACIÓN DE CAMINATA
    # ========================================================

    if current_direction is not None:

        animation_timer += 1


        if animation_timer >= animation_speed:

            animation_timer = 0

            animation_frame += 1


            # Volver al primer frame
            # para crear un ciclo continuo.

            if animation_frame >= 4:

                animation_frame = 0


        player_image = animations[
            current_direction
        ][animation_frame]


    # ========================================================
    # LIMITES DE LA PANTALLA
    # ========================================================

    if player_x < 0:

        player_x = 0


    if player_x > WIDTH - player_size:

        player_x = WIDTH - player_size


    if player_y < 0:

        player_y = 0


    if player_y > HEIGHT - player_size:

        player_y = HEIGHT - player_size


    # ========================================================
    # DIBUJAR FONDO
    # ========================================================

    screen.blit(
        background,
        (0, 0)
    )


    # ========================================================
    # DIBUJAR PERSONAJE
    # ========================================================

    screen.blit(
        player_image,
        (player_x, player_y)
    )


    # ========================================================
    # TEXTO DE EXPRESIÓN
    # ========================================================

    if expression is None:

        expression_text = "SIN ROSTRO"

    else:

        expression_text = expression


    # ========================================================
    # TEXTO DE MOVIMIENTO
    # ========================================================

    if command is None:

        command_text = "---"

    else:

        command_text = command


    # ========================================================
    # CREAR TEXTOS
    # ========================================================

    expression_surface = font.render(
        f"EXPRESION: {expression_text}",
        True,
        COLOR_BLANCO
    )


    command_surface = font.render(
        f"MOVIMIENTO: {command_text}",
        True,
        COLOR_BLANCO
    )


    # ========================================================
    # MOSTRAR TEXTOS
    # ========================================================

    screen.blit(
        expression_surface,
        (20, 20)
    )


    screen.blit(
        command_surface,
        (20, 55)
    )


    # ========================================================
    # ACTUALIZAR PANTALLA
    # ========================================================

    pygame.display.flip()


    # ========================================================
    # FPS
    # ========================================================

    clock.tick(30)


# ============================================================
# CERRAR
# ============================================================

controller.release()

pygame.quit()