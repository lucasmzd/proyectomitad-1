import pygame
from funciones import *
from constantes import *
from preguntas import lista_preguntas
from menu import *
from juego import *
from ajustes import *
from terminado import *
from ranking import *
from categoria import *
from dificultad import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS")
pantalla = pygame.display.set_mode(PANTALLA)
pygame.display.set_icon(pygame.image.load("texturas/icono.png"))
reloj = pygame.time.Clock()
datos_juego = crear_datos_juego()
ventana_actual = "menu"
bandera_juego = False
lista_rankings = []
categoria_elegida = None
dificultad_elegida = "normal"

while True:
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            ventana_actual = "salir"
    if ventana_actual == "menu":
        ventana_actual = mostrar_menu(pantalla, cola_eventos)
    elif ventana_actual == "jugar":
        ventana_actual = "categoria"
    elif ventana_actual == "categoria":
        ventana_actual = mostrar_categoria(pantalla, cola_eventos)
        if ventana_actual in ["entretenimiento", "deporte", "ciencia", "historia", "geografia", "arte"]:
            categoria_elegida = ventana_actual
            random.shuffle(lista_preguntas)
            reiniciar_estadisticas(datos_juego)
            establecer_dificultad(datos_juego, dificultad_elegida)
            bandera_juego = True
            ventana_actual = "juego"
    elif ventana_actual == "dificultad":
        eleccion = mostrar_dificultad(pantalla, cola_eventos)
        if eleccion in ["facil", "normal", "dificil"]:
            dificultad_elegida = eleccion
            establecer_dificultad(datos_juego, dificultad_elegida)
            ventana_actual = "menu"
    elif ventana_actual == "juego":
        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego, categoria_elegida)
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos, lista_rankings)
    elif ventana_actual == "terminado":
        if bandera_juego:
            pygame.mixer.music.stop()
            bandera_juego = False
        ventana_actual = mostrar_game_over(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "salir":
        break
    pygame.display.flip()
pygame.quit()