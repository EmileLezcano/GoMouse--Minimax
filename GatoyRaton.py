import pygame
import sys



# Inicializar Pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

# Dimensiones del tablero
FILAS = 5
COLUMNAS = 5
TAMANO_CELDA = 100  # Tamaño de cada celda

# Tamaño de la pantalla
ANCHO_PANTALLA = COLUMNAS * TAMANO_CELDA
ALTO_PANTALLA = FILAS * TAMANO_CELDA

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('GoMouse!')

# Cargar imagen de los personajes y ajustar tamaño
raton_img = pygame.image.load("./img/raton.png")  # Ruta de la imagen del personaje
raton_img = pygame.transform.scale(raton_img, (TAMANO_CELDA, TAMANO_CELDA))  # Ajustar tamaño

gato_img = pygame.image.load("./img/gato.png")  # Ruta de la imagen del segundo personaje
gato_img = pygame.transform.scale(gato_img, (TAMANO_CELDA, TAMANO_CELDA))  # Ajustar tamaño

casa_img = pygame.image.load("./img/casa.png")  # Ruta de la imagen del tercer personaje
casa_img = pygame.transform.scale(casa_img, (TAMANO_CELDA, TAMANO_CELDA))  # Ajustar tamaño

# Posiciones de los personajes
posicion_raton = [0, 4]  # Celda (0, 4)
posicion_gato = [0, 0]  # Celda (0, 0)
posicion_casa = [4, 2]  # Celda (4, 2)

# Variable para controlar el turno
turno_raton = True  # Empieza el raton

# Definir las direcciones de movimiento
DIRECCIONES = {
    'arriba': (-1,0),
    'abajo': (1,0),
    'izquierda': (0,-1),
    'derecha': (0,1)
}

# Evaluar estado del juego
def evaluar_estado(pos_raton, pos_gato):
    # la distancia de Manhattan nos dirá cuántos movimientos necesitamos para llegar de un punto a otro.
    return abs(pos_raton[0] - pos_gato[0]) + abs(pos_raton[1] - pos_gato[1])

#Obtener movimientos posibles
def obtener_movimientos(pos):
    movimientos = []
    for direccion, (dx, dy) in DIRECCIONES.items():
        nuevo_x = pos[0] + dx
        nuevo_y = pos[1] + dy
        if 0 <= nuevo_x < FILAS and 0 <= nuevo_y < COLUMNAS:
            movimientos.append((direccion, (nuevo_x,nuevo_y)))
    return movimientos

# Implementar Minimax
def minimax(pos_raton, pos_gato, profundidad, es_turno_gato):
    if profundidad == 0 or pos_raton == pos_gato:
        return evaluar_estado(pos_raton, pos_gato)
    
    if es_turno_gato:
        mejor_valor = float('inf')
        for _, nueva_pos in obtener_movimientos(pos_gato):
            valor = minimax(pos_raton, nueva_pos, profundidad - 1, False)
            mejor_valor = min(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('-inf')
        for _, nueva_pos in obtener_movimientos(pos_raton):
            valor = minimax(nueva_pos, pos_gato, profundidad - 1, True)
            mejor_valor = max(mejor_valor, valor)
        return mejor_valor

# Obtener el mejor movimiento para el gato
def mejor_movimiento_gato(pos_raton, pos_gato):
    mejor_mov = None
    mejor_valor = float('inf')
    for direccion, nueva_pos in obtener_movimientos(pos_gato):
        valor = minimax(pos_raton, nueva_pos, 6, False)
        if valor < mejor_valor:
            mejor_valor = valor
            mejor_mov = direccion
    return mejor_mov

# Bucle principal del juego
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar eventos de presión de tecla para mover el raton
        if evento.type == pygame.KEYDOWN:
            if turno_raton:
                if evento.key == pygame.K_LEFT and posicion_raton[1] > 0:
                    posicion_raton[1] -= 1
                    turno_raton = False
                if evento.key == pygame.K_RIGHT and posicion_raton[1] < COLUMNAS - 1:
                    posicion_raton[1] += 1
                    turno_raton = False
                if evento.key == pygame.K_UP and posicion_raton[0] > 0:
                    posicion_raton[0] -= 1
                    turno_raton = False
                if evento.key == pygame.K_DOWN and posicion_raton[0] < FILAS - 1:
                    posicion_raton[0] += 1
                    turno_raton = False

    # Mover gato usando Minimax si no es el turno del raton
    if not turno_raton:
        mejor_mov = mejor_movimiento_gato(posicion_raton, posicion_gato)
        if mejor_mov:
            dx, dy = DIRECCIONES[mejor_mov]
            posicion_gato[0] += dx
            posicion_gato[1] += dy
        turno_raton = True


    # Verificar si el raton está en la celda (4, 2)
    if posicion_raton == posicion_casa:
        print("GANASTE! DISFRUTA TU PIZZA 🍕╰(*°▽°*)╯")
        pygame.quit()
        sys.exit()
    
    # Verificar si el personaje2 esta en la misma celda que el personaje1
    if posicion_raton == posicion_gato:
        print("GAME OVER 😼 (┬┬﹏┬┬)")
        pygame.quit()
        sys.exit()


    pantalla.fill(BLANCO)  # Color de fondo

    # Dibujar el tablero
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = NEGRO if (fila + columna) % 2 == 0 else AZUL  # Alternar colores
            pygame.draw.rect(pantalla, color, (columna * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    # Dibujar los personajes en sus respectivas celdas
    pantalla.blit(raton_img, (posicion_raton[1] * TAMANO_CELDA, posicion_raton[0] * TAMANO_CELDA))
    pantalla.blit(gato_img, (posicion_gato[1] * TAMANO_CELDA, posicion_gato[0] * TAMANO_CELDA))
    pantalla.blit(casa_img, (posicion_casa[1] * TAMANO_CELDA, posicion_casa[0] * TAMANO_CELDA))

    pygame.display.flip()  # Actualizar pantalla
